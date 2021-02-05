import digitalocean
import fnmatch
import subprocess
import config

class Axiom():
    def __init__(self):
        self.do_api = config.Config().do_api
        self.manager = digitalocean.Manager(token=self.do_api)
        self.limit = self.manager.get_account().droplet_limit
        self.name = ""
        self.instances = []    # List of axiom instances
        self.axiom_count = 0    # How many axiom instances are available

    def get_all_instances(self):
        return self.manager.get_all_droplets()

    def select(self, name):
        # Get the axiom instances to use for concurrency
        droplets = self.get_all_instances()
        self.name = name
        self.instances = []
        for d in droplets:
            if fnmatch.filter([d.name], f"{self.name}*"):
                self.instances.append(d.name)
        # Save the available number of instances
        self.axiom_count = len(self.instances)
        return self.instances

    def exec(self, command):
        results = []
        if self.axiom_count > 0:
            self.select(self.name)
            for i in self.instances:
                self.axiom_count -= 1
                r = subprocess.run(
                    f"axiom-exec {command} {i}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
                results += r.stdout.decode('utf-8')
        return results

    def fleet(self, count):
        r = subprocess.run(
                f"axiom-fleet {self.name} -i={count}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )
        self.select(self.name)
        return r.stdout.decode('utf-8')

    def remove(self, selection):
        # axiom-rm is not reliable, so DO NOT allow the use of wildcards
        if "*" in selection:
            return "ERROR: Instance name includes wildcards."
        else:
            r = subprocess.run(
                    f"axiom-rm {selection} -f",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
            return r.stdout.decode('utf-8')

    def send(self, src, dest, instance):
        # Sends a file to an instance.
        r = subprocess.run(
                    f"axiom-scp {src} {instance}:{dest}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
        return r.stdout.decode('utf-8')

    def get(self, src, dest, instance):
        # Gets a file from an instance.
        r = subprocess.run(
                    f"axiom-scp {instance}:{src} {dest}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
        return r.stdout.decode('utf-8')