class ParkingSlot:
    def __init__(self, floor, index, slot_type):
        self.floor = floor
        self.index = index
        self.type = slot_type
        self.occupied = False
        self.vehicle = None

    def occupy(self, vehicle):
        if self.occupied:
            return False
        if not vehicle.matches(self):
            return False
        self.occupied = True
        self.vehicle = vehicle
        return True

    def vacate(self):
        if not self.occupied:
            return None
        v = self.vehicle
        self.occupied = False
        self.vehicle = None
        return v

    def getlocation(self):
        return f"Floor {self.floor}, Slot {self.index}"

class Vehicle:
    
    def __init__(self, vehicleNumber, vehicletype, ownername, entrytime):
        self.vehicleNumber = vehicleNumber
        self.vehicletype = vehicletype
        self.ownername = ownername
        self.entrytime = entrytime

    def gettype(self):
        return self.vehicletype

    def matches(self, slot: ParkingSlot):
        type_map = {1: '4 wheeler', 2: '2 wheeler', 3: '3 wheeler'}
        want = type_map.get(self.vehicletype)
        return (not slot.occupied) and (slot.type == want)

class Ticket:
    def __init__(self):
        self.closed = False

    def generatebill(self, vehicle, duration, amount):
        return {
            'vehicleNumber': vehicle.vehicleNumber,
            'owner': vehicle.ownername,
            'duration': duration,
            'amount': amount
        }

    def close(self):
        self.closed = True

class BillingEngine:
    def __init__(self):
        self.passes = {}

    def comutecharge(self, duration, vehicletype):
        rates = {1: 10, 2: 5, 3: 20}
        rate = rates.get(vehicletype, 10)
        hrs = max(1, int(duration))
        return rate * hrs

    def applypass(self, vehicleNumber):
        p = self.passes.get(vehicleNumber)
        return bool(p)

    def add_pass(self, vehicleNumber):
        self.passes[vehicleNumber] = True

    def revoke_pass(self, vehicleNumber):
        self.passes.pop(vehicleNumber, None)

class ParkingLot:
    def __init__(self):
        self.floors = [] 
        self.ticket_engine = Ticket()
        self.billing = BillingEngine()

    def addfloor(self, slots_spec):
        floor_index = len(self.floors)
        floor = []
        for i, t in enumerate(slots_spec):
            floor.append(ParkingSlot(floor_index, i, t))
        self.floors.append(floor)
        return floor_index

    def findslot(self, vehicleNumber=None, vehicletype=None):
        
        if vehicleNumber is not None:
            for floor in self.floors:
                for s in floor:
                    if s.occupied and s.vehicle and getattr(s.vehicle, 'vehicleNumber', None) == vehicleNumber:
                        return (s.floor, s.index)
            return None

       
        if vehicletype is not None:
            type_map = {1: '2 wheeler',2:'3 wheeler'}
            want = type_map.get(vehicletype)
            if want is None:
                return None
            for floor in self.floors:
                for s in floor:
                    if not s.occupied and s.type == want:
                        return (s.floor, s.index)
            return None

        free = []
        for floor in self.floors:
            for s in floor:
                if not s.occupied:
                    free.append((s.floor, s.index, s.type))
        return free
    
    def getoccupancy(self):
        total = 0
        occupied = 0
        by_type = {}
        for floor in self.floors:
            for s in floor:
                total += 1
                by_type.setdefault(s.type, {'total': 0, 'occupied': 0})
                by_type[s.type]['total'] += 1
                if s.occupied:
                    occupied += 1
                    by_type[s.type]['occupied'] += 1
        return {'total': total, 'occupied': occupied, 'free': total - occupied, 'by_type': by_type}

if __name__ == "__main__":
    
    vehicleNumber = input("Enter your vehicle number: ")
    vehicletype = int(input("Enter the type of vehicle (1=4 wheeler,2=2 wheeler,3=3 wheeler): "))
    ownername = input("Enter the name of the owner: ")
    entrytime = int(input("Enter the time of arrival (hour integer): "))
    exittime = int(input("Enter the time of departure (hour integer): "))
    
    lot = ParkingLot()
    lot.addfloor(['4 wheeler','4 wheeler','2 wheeler'])
    lot.addfloor(['3 wheeler', '4 wheeler', '2 wheeler'])
    veh = Vehicle(vehicleNumber, vehicletype, ownername, entrytime)
    allocated = False
    for floor in lot.floors:
        for slot in floor:
            if veh.matches(slot):
                if slot.occupy(veh):
                    allocated = slot
                    break
        if allocated:
            break

    if allocated:
        print("Parked at:", allocated.getlocation())
        print("Occupancy:", lot.getoccupancy())
        print("charge:", lot.billing.comutecharge(duration=exittime - entrytime, vehicletype=vehicletype))
    else:
        print("No suitable slot available.")
