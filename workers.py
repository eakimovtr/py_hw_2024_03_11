import uuid

class Employee:
    
    def __init__(self, name: str, rate: float):
        self.name: str = name
        self.rate: float = rate
        self.number: str = str(uuid.uuid4())[:8]
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.number})"


class ProductionWorker(Employee):
    
    # Every new worker is initialized with the object of his shift
    def __init__(self, name: str, rate: float, shift):
        super().__init__(name, rate)
        shift.add_worker(self)

    def get_shift(self) -> int:
        return self.number_of_shift

    def change_shift(self, shift: int) -> None:
        self.number_of_shift = shift if shift in (1, 2) else "Error"

    def salary(self) -> float:
        match self.number_of_shift:
            case 1:
                return self.rate * 8
            case 2:
                return self.rate * 8 * 1.5


class ShiftSupervisor(Employee):
    def __init__(self, name: str, rate: float):
        super().__init__(name, rate)
        
        
class Shift:
    
    # There can be only one supervisor for one shift, but many workers (one to many)
    def __init__(self, no: int, supervisor: ShiftSupervisor, *workers: ProductionWorker):
        self.__no = no
        self.__supervisor: ShiftSupervisor = supervisor
        self.__workers: list[ProductionWorker] = list(workers)

    def get_no(self) -> int:
        return self.__no
    
    def get_supervisor(self) -> ShiftSupervisor:
        return self.__supervisor
    
    def get_workers(self) -> list[ProductionWorker]:
        return self.__workers
    
    def set_supervisor(self, supervisor: ShiftSupervisor) -> None:
        self.__supervisor = supervisor
    
    def add_worker(self, worker: ProductionWorker) -> None:
        self.__workers.append(worker)
        
    def exclude_worker(self, worker: ProductionWorker) -> None:
        for w in self.__workers:
            if w == worker:
                self.__workers.remove(w)
        else:
            raise f"No such worker on shift {self.get_no()}"
        
    def __repr__(self) -> str:
        return f"Shift {self.get_no()} ( {self.get_supervisor()}, {self.get_workers()} )"
        

class Fabric:
    @staticmethod
    def demo():
        boss_1 = ShiftSupervisor("Big Boss", 8.99)
        boss_2 = ShiftSupervisor("Small Boss", 6.99)

        shift_1 = Shift(1, boss_1)
        shift_2 = Shift(2, boss_2)


        ProductionWorker("Lox", 1, shift_1)
        ProductionWorker("Kek", 2.2, shift_1)
        ProductionWorker("Bob", 3, shift_1)
        ProductionWorker("Rob", 1.6, shift_1)

        ProductionWorker("Tom", 3, shift_2)
        ProductionWorker("Jones", 1.5, shift_2)
        ProductionWorker("Katie", 1.8, shift_2)

        print(shift_1)
        print(shift_2)
        
        
Fabric.demo()