#!/bin/bash

# Set the main variables
set -a
source "$HOME"/gatherecon/configs/tokens.ini || return

YELLOW="\e[33m"
GREEN="\e[32m"
RED="\e[31m"
MAGENTA="\e[35m"
CYAN="\e[36"
RESET="\e[0m"
DOMAIN="$1"
SCOPE="$2"
TODATE=$(date +"%Y-%m-%d")
FOLDERNAME=recon-$TODATE
RESULTDIR="$HOME/assets/$DOMAIN/$FOLDERNAME"
SUBS="$RESULTDIR/subdomains"
WORDLIST="$RESULTDIR/wordlists"
IPS="$RESULTDIR/ips"
TOOLS="$HOME/tools"
MODE=active
SECONDS=0

try() {
    "$@" || {e=$?; echo "ERROR: ${@}"; exit $e}
}

startFunction() {
    tool=$1
    echo -e "\n[${GREEN}+${RESET}] Starting $tool"
}

download() {
    git_tools=(
        "https://github.com/Abss0x7tbh/bass"
        "https://github.com/projectdiscovery/subfinder"
        "https://github.com/gwen001/github-subdomains"
        "https://github.com/OWASP/Amass"
        "https://github.com/hakluke/hakrawler"
        "https://github.com/m8r0wn/subscraper"
        "https://github.com/projectdiscovery/shuffledns"
        "https://github.com/ponderng/nscope"
    )
    for i in "${git_tools[@]}"
    do
        cd $TOOLS
        j=${i##*/}  #This will capture the basename without a call
        result=0
        if [ ! -d $j/.git ]; then
            # If not already, then clone the repo
            try /usr/bin/git clone $i
            result=$?
        else
            echo "${i} already exists"
        fi
    done
}

install() {
    # Download anything needed
    # and run any setup files
    mkdir -p $TOOLS
    cd $TOOLS
    export GO111MODULE=on

    # "https://github.com/projectdiscovery/subfinder"
    go get -u -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder

    # "https://github.com/gwen001/github-subdomains"
    go get -u github.com/gwen001/github-subdomains

    # "https://github.com/OWASP/Amass"
    go get -v github.com/OWASP/Amass/v3/...

    # "https://github.com/hakluke/hakrawler"
    go get github.com/hakluke/hakrawler

    # "https://github.com/m8r0wn/subscraper"
    git clone https://github.com/m8r0wn/subscraper
    python3 subscraper/setup.py install

    # "https://github.com/projectdiscovery/shuffledns"
    go get -u -v github.com/projectdiscovery/shuffledns/cmd/shuffledns

    # "https://github.com/ponderng/nscope"
    git clone https://github.com/ponderng/nscope.git

    # "https://github.com/Abss0x7tbh/bass"
    git clone https://github.com/Abss0x7tbh/bass.git
    python3 -m pip install -r bass/requirements.txt

    exit 0
}

usage() { 
    echo "Usage:"
    echo "    -d            Domain to discover subdomains from"
    echo "    -s            BurpSuite scope file to validate subdomains with"
    echo "    -a            Active recon mode"
    echo "    --install     Install and verify needed tools"
    exit 1
}

# Display help text when no arguments are given, otherwise process arguments
PARSED_ARGUMENTS=$(getopt --options d:s:a --long install -- "$@")
VALID_ARGUMENTS=$?
if [ "$VALID_ARGUMENTS" != "0" ]; then
    usage
fi
eval set -- "$PARSED_ARGUMENTS"
while true; do
    case "$1" in
        -d) #### Domain to retrieve subdomains from
            DOMAIN="$2"
            shift 2
            echo "Domain: ${DOMAIN}"
            ;;
        -s) #### Process JSON scope files from BurpSuite for URL lists
            SCOPE="$2"
            shift 2
            echo "Scope: ${SCOPE}"
            ;;
        -a) #### active recon mode
            MODE=active
            ;;
        --install)  #### install and verify
            install
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Invalid option: $1 requires an argument" 1>&2
            usage
            ;;
    esac
done

if [[ -z $DOMAIN ]]; then
    usage
    exit 1
fi

# Begin subdomain enumeration
echo -e "${MAGENTA}\n--==[ Starting Subdomain Enumeration ]==--${RESET}"
echo -e "[${GREEN}+${RESET}] Mode: ${RED}${MODE}${RESET}"

# Check for target directories and create them if missing
for dir in \
    "$RESULTDIR" \
    "$SUBS" \
    "$WORDLIST" \
    "$IPS"
do
    if [ ! -d "$dir" ]; then
        echo -e "${RED} Creating directory ${dir}${RESET}"
        mkdir -p "$dir"
    fi
done

# Gather resolvers
startFunction "bass (resolvers)"
cd "$TOOLS"/bass || return
python3 bass.py -d "$DOMAIN" -o "$IPS"/resolvers.txt

startFunction "subfinder"
"$HOME"/go/bin/subfinder -d "$DOMAIN" -config "$HOME"/gatherecon/configs/subfinder.yaml -o "$SUBS"/subfinder.txt
echo -e "[${GREEN}+${RESET}] Done."

# Github gives different result sometimes, so running multiple instances so that we don't miss any subdomain
startFunction "github-subdomains"
github-subdomains -t $github_subdomains_token -d "$DOMAIN" | sort -u >> "$SUBS"/github_subdomains.txt
sleep 5
github-subdomains -t $github_subdomains_token -d "$DOMAIN" | sort -u >> "$SUBS"/github_subdomains.txt
sleep 5
github-subdomains -t $github_subdomains_token -d "$DOMAIN" | sort -u >> "$SUBS"/github_subdomains.txt
echo -e "[${GREEN}+${RESET}] Done."

# Using passive mode in amass to stop it from resolving subdomains
startFunction "amass"
"$HOME"/go/bin/amass enum -passive -dir "$SUBS"/amass -d "$DOMAIN" -config "$HOME"/gatherecon/configs/amass.ini -oA "$SUBS"/amass_scan
echo -e "[${GREEN}+${RESET}] Done."

# Do active scans against the target if enabled
if [ "$MODE" = "active" ]; then
    # We don't need everything from hakrawler, since we're only after subdomains
    startFunction "hakrawler"
    hakrawler -js -linkfinder -subs -depth 2 -scope subs -url "$DOMAIN" -outdir "$SUBS"/hakrawler
    for req in "$SUBS/hakrawler/*"
    do
        awk '/Host:/ {print $2;}' $req >> "$SUBS"/hakrawler.txt
    done
    echo -e "[${GREEN}+${RESET}] Done."

    # Subscraper
    startFunction "Subscraper"
    "$TOOLS"/subscraper/subscraper.py -u "$DOMAIN" -o "$SUBS"/subscraper.txt
    echo -e "[${GREEN}+${RESET}] Done."
fi

echo -e "\n[${GREEN}+${RESET}] Combining and sorting results.."
cat "$SUBS"/*.txt | sort -u >"$SUBS"/subdomains

# Resolving domains to prune out the ones that won't resolve
# using shuffledns since amass choked up on the resolver list
echo -e "\n[${GREEN}+${RESET}] Resolving All Subdomains.."
shuffledns -list "$SUBS"/subdomains -silent -d "$DOMAIN" -r "$IPS"/resolvers.txt -o "$SUBS"/all_subdomains
echo -e "[${GREEN}+${RESET}] Done."

# Check subdomains against scope file if given
if [ ! -z $SCOPE ]; then
    echo -e "\n[${GREEN}+${RESET}] Checking subdomains against scope.."
    "$TOOLS"/nscope/nscope -t "$SUBS"/all_subdomains -s "$SCOPE" -o "$SUBS"/all_subdomains
    echo -e "[${GREEN}+${RESET}] Done."
fi

echo -e "${MAGENTA}\n--==[ Finished Subdomain Enumeration ]==--${RESET}"

DURATION=$SECONDS
echo -e "${RED}\n Scan completed in : $(($DURATION / 60)) minutes and $(($DURATION % 60)) seconds.${RESET}"
exit 0