import paho.mqtt.client as mqtt
from config import BROKER
import json
from utils import euclidean_distance


class Communication:
    """Handles MQTT communication."""
    def __init__(self, teamname):
        self.teamname = teamname
        self.publisher = mqtt.Client(f'{teamname}_publisher')
        self.subscriber = mqtt.Client(f'{teamname}_subscriber')
        self.publisher.connect(BROKER)
        self.subscriber.connect(BROKER)
        self.publisher.loop_start()
        self.subscriber.loop_start()
        self.pitstop_coords = {}
        self.start_coords = {}
        self.understanding_msgs = {}
        self.verified_teams = []

    def subscribe_all(self):
        self.subscribe_discovery()
        # Call all your subscriber methods here

    def subscribe_discovery(self):
        self.subscriber.subscribe('lab5/discovery')

    def subscribe_coordinates(self):
        """Subscribe to pit-stop and starting position coordinate topics."""

    
    def subscribe_in(self):
        """Subscribe to the 'lab5/<own_teamname>/in' topic of your team."""


    def subscribe_understanding(self):
        """Subscribe to the understanding topics in consensus.
        
        That is, lab5/consensus/understanding and
        lab5/consensus/understanding/ok topics."""

    def populate_pitstops(self, topic, msg):
        """Update pitstop information"""
        
    def populate_starts(self, topic, msg):
        n = topic[-1]
        data = json.loads(msg)
        self.start_coords[int(n)] = [data['x'], data['y']]
        # print(self.start_coords)

    def populate_understanding(self, topic, msg):
        """Fills the understanding message datastructure."""

    def publish_all(self):
        self.publish_understanding()
        # Call all your subscriber methods here

    def publish_discovery(self):
        """Publish team info to discovery topic."""

    def publish_understanding(self):
        """Demonstrate your understanding of the problem.

        Compute the distance between each of the pit-stops to each of the 
        starting points. Then publish the corresponding message to the
        consensus understanding topic."""
        
        if len(self.pitstop_coords) == 3 and len(self.start_coords) == 3:
            data = {'teamname': self.teamname}
            for np, (xp, yp) in self.pitstop_coords.items():
                data[f'pitstop{np}'] = {}
                for ns, (xs, ys) in self.start_coords.items():
                    data[f'pitstop{np}'][f'start{ns}'] = euclidean_distance(xp, yp, xs, ys)
            data = json.dumps(data)
            self.publisher.publish('lab5/consensus/understanding', data)
    
    def publish_understanding_ok(self):
        """Checks if all the understanding information is present and publishes
        the relevant message."""

        # This works only if you are handling duplicates
        if len(self.understanding_msgs) == 3:
            ...
            # Your publishing code


class LeaderCommunication(Communication):
    def subscribe_all(self):
        super().subscribe_all()
        self.subscribe_race_go()

    def subscribe_race_go(self):
        self.subscriber.subscribe('lab5/race/go')

    def verify_understanding(self, topic, msg, teammates):
        """Leader verifies the understanding.
        
        Publish to teammate 'in' topics if correct, else to the consensus
        'fail' topic."""
        data = json.loads(msg)
        for k in data['verified']:
            if k not in self.verified_teams:
                self.verified_teams.append(k)
        
        # Add rest of the logic/code here

    
    def check_race_go(self, topic, msg, teammates):
        """Publish the 'go1' message to teammates."""
