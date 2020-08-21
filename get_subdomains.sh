#!/bin/bash

# Set the main variables
set -a
source "$HOME"/GatherRecon/configs/tokens.txt || return

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
MODE=active
SECONDS=0

startFunction() {
    tool=$1
    echo -e "\n[${GREEN}+${RESET}] Starting $tool"
}

usage() { 
    echo "Usage:"
    echo "    -d            Domain to discover subdomains from"
    echo "    -s            BurpSuite scope file to validate subdomains with"
    echo "    -p            active recon mode"
    exit 1
}

# Display help text when no arguments are given, otherwise process arguments
while getopts ":d:s:p" opt; do
    case "${opt}" in
        d) #### Domain to retrieve subdomains from
            DOMAIN=${OPTARG}
            ;;
        s) #### Process JSON scope files from BurpSuite for URL lists
            SCOPE=${OPTARG}
            ;;
        a) #### active recon mode
            MODE=active
            ;;
        \?)
            usage
            ;;
        :)
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            ;;
    esac
done
shift $((OPTIND - 1))

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
cd "$HOME"/tools/bass || return
python3 bass.py -d "$DOMAIN" -o "$IPS"/resolvers.txt

startFunction "subfinder"
"$HOME"/go/bin/subfinder -d "$DOMAIN" -config "$HOME"/GatherRecon/configs/subfinder.yaml -o "$SUBS"/subfinder.txt
echo -e "[${GREEN}+${RESET}] Done."

# Github gives different result sometimes, so running multiple instances so that we don't miss any subdomain
startFunction "github-subdomains"
python3 "$HOME"/tools/github-subdomains.py -t $github_subdomains_token -d "$DOMAIN" | sort -u >> "$SUBS"/github_subdomains.txt
sleep 5
python3 "$HOME"/tools/github-subdomains.py -t $github_subdomains_token -d "$DOMAIN" | sort -u >> "$SUBS"/github_subdomains.txt
sleep 5
python3 "$HOME"/tools/github-subdomains.py -t $github_subdomains_token -d "$DOMAIN" | sort -u >> "$SUBS"/github_subdomains.txt
echo -e "[${GREEN}+${RESET}] Done."

# Using passive mode in amass to stop it from resolving subdomains
startFunction "amass"
"$HOME"/go/bin/amass enum -passive -dir "$SUBS"/amass -d "$DOMAIN" -config "$HOME"/GatherRecon/configs/amass.ini -oA "$SUBS"/amass_scan
echo -e "[${GREEN}+${RESET}] Done."

# Do active scans against the target if enabled
if [ "$MODE" = "active" ]; then
    # We don't need everything from hakrawler, since we're only after subdomains
    hakrawler -js -linkfinder -subs -depth 1 -url "$DOMAIN" -outdir "$SUBS"/hakrawler
    for req in "$SUBS/hakrawler/*"
    do
        awk '/Host:/ {print $2;}' $req >> "$SUBS"/hakrawler.txt
    done
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
    "$HOME"/tools/nscope -t "$SUBS"/all_subdomains -s "$SCOPE" -o "$SUBS"/all_subdomains
    echo -e "[${GREEN}+${RESET}] Done."
fi

echo -e "${MAGENTA}\n--==[ Finished Subdomain Enumeration ]==--${RESET}"

DURATION=$SECONDS
echo -e "${RED}\n Scan completed in : $(($DURATION / 60)) minutes and $(($DURATION % 60)) seconds.${RESET}"
