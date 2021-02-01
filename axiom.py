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

    def select_instances(self):
        # Get the axiom instances to use for concurrency
        droplets = self.get_all_instances()
        for d in droplets:
            if fnmatch.filter([d.name], f"{self.name}*"):
                self.instances += d.name
        # Save the available number of instances
        self.axiom_count = len(self.instances)
        return self.instances

    def exec(self, command):
        results = []
        if self.axiom_count > 0:
            self.select_instances()
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
        return r.stdout.decode('utf-8')

    def remove(self, selection):
        r = subprocess.run(
                f"axiom-rm {selection} -f",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True
            )
        return r.stdout.decode('utf-8')