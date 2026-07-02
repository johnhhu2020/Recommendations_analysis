import sys
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict


@dataclass
class Event:
    ts: datetime
    role_id: int
    action: str
    item_id: int


class EventParser:
    '''Seperate fields to: t_when, role_id, action, itemid
    '''
    def parser(self, line:str) -> Event:
        parts = line.split()
        # prinnt(parts)
        iso_str = f"{parts[0]}T{parts[1]}"

        return Event(
            ts = datetime.fromisoformat(iso_str),
            # dump ts = datetime.strptime(f"{parts[0]} {parts[1]}", "%Y-%m-%d %H:%M:%S"),
            role_id = int(parts[2]),
            action = parts[3],
            item_id = int(parts[4])
            )


class EventSearch:
    '''State machine searching
    '''
    def __init__(self):
        self.states = defaultdict(lambda: defaultdict(lambda: {
            "rec_time": None,
            "first_look": None,
            "buy_time": None
        }))

    def search(self, event: Event):
        action = event.action
        item_id = event.item_id
        ts = event.ts
        role_id = event.role_id
        
        if action == "rec":
            print("rec part is running")
            
            # Any rec for new item breaks the current rec circle for this user
            active_rec_items = list(self.states[role_id].keys())
            #active_rec_items = list(next(iter(self.states[role_id])))
            print(f"active items: {active_rec_items}")
            
            for active_rec_item in active_rec_items:
                if active_rec_item != item_id:
                    print(f"rec: {active_rec_item} circle broken by: {item_id}")

                    del self.states[role_id][active_rec_item]

            state = self.states[role_id][item_id]
            state["rec_time"] = ts
            state["first_look"] = None
            
            print(
                f"role_id: {role_id}, item_id: {item_id}, rec_time: {state['rec_time']}")
            #rint(f"states: {self.states}")
            

        elif action == "look":
            print("look part is running")

            if (role_id in self.states 
            and item_id in self.states[role_id]):

                state = self.states[role_id][item_id]

                if state["first_look"] is None:
                    state["first_look"] = ts
                    
                    print(
                        f"role_id: {role_id}, item_id: {item_id}, rec_time: {state['rec_time']}, first_look: {state['first_look']}")


        elif action == "buy":
            print("buy part is running")

            if (role_id in self.states 
            and item_id in self.states[role_id]):

                state = self.states[role_id][item_id]
                
                if state["first_look"] is not None:

                    state["buy_time"] = ts
                    
                    # Funnel complete, packaging results
                    output = (
                        role_id, item_id, state["rec_time"], state["first_look"], state["buy_time"]
                        )
                    print(
                        f"role_id: {role_id}, item_id: {item_id}, rec_time: {state['rec_time']}, first_look: {state['first_look']}, buy_time: {state['buy_time']}")

                    del self.states[role_id][item_id]

                    return output

                else:
                    # In case there is not look between rec and buy
                    print(f"no look before buy, role_id: {role_id}, item_id: {item_id}")
                    del self.states[role_id][item_id]


class RecSearch:
    '''Pipeline
    input_file: 
        the log file which may containing rec events stream of many users
    output_file:
        role_id, item_id, rec_time, first_look_time, buy_time
    classes used:
        EventParser, EventSearch 
    '''
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.event_parser = EventParser()
        self.event_search = EventSearch()

    def run(self):
        with open(self.input_file, "r") as f, open(self.output_file, "w") as output:
            output.write("role_id,item_id,rec_time,first_look_time,buy_time\n")
            
            next(f)
            for line in f:
                events = self.event_parser.parser(line)
                if events is None:
                    continue

                complete = self.event_search.search(events)

                # Why we need this
                if complete is None:
                    continue 

                output.write(f"{complete[0]}, {complete[1]},{complete[2]},{complete[3]},{complete[4]}\n")


if __name__ == "__main__":
    Rec_Search = RecSearch(sys.argv[1], sys.argv[2])
    Rec_Search.run()
