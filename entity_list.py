class EntityList:
    def __init__(self):
        self.entities = []
        self.queue = []


    def __getitem__(self, s):
        return self.entities.__getitem__(s)


    def __setitem__(self, s, o):
        return self.entities.__setitem__(s, o)


    def __delitem__(self, i):
        return self.entities.__delitem__(i)


    def __iter__(self):
        return self.entities.__iter__()


    def index(self, entity):
        return self.entities.index(entity)

    def append(self, entity):
        self.entities.append(entity)
        if entity.fighter:
            self.queue.append({"entity": entity, "points": 0})


    def dequeue(self, entity):
        candidates = [item for item in self.queue if item["entity"] is entity]
        if len(candidates):
            for x in candidates:
                self.queue.remove(x)


    def remove(self, entity):
        if entity in self.entities:
            self.dequeue(entity)
            self.entities.remove(entity)        

    
    def get_ready(self):
        while True:
            ready = [item for item in self.queue if item["points"] >= 100]
            if ready:
                break

            for item in self.queue:
                entity = item["entity"]
                if entity.fighter and entity.fighter.speed:
                    item["points"] += entity.fighter.speed

        entities = []
        for item in ready:
            item["points"] = 0
            entities.append(item["entity"])
        
        return entities