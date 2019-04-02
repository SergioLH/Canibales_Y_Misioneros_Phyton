class MissionariesState:
    """
    This class is used to represent a state of the missionaries
    and cannibals problem. Each state contains the number of
    missionaries and cannibals in each shore, the position
    of the boat, and the capacity of the boat to determine
    whether a state is valid or not.
    """

    def __init__(self, left_miss, left_cann, right_miss, right_cann, boat_position, capacity=2):
        self.miss = (left_miss, right_miss)  # missionaries in left and right shores
        self.cann = (left_cann, right_cann)  # cannibals in left and right shores
        self.boat_position = boat_position   # boat position ('left', 'right')
        self.capacity = capacity             # boat capacity (missionaries+cannibals)

    def __str__(self):
        to_str = "(%d, %d)" % (self.miss[0], self.cann[0])
        if self.boat_position == "left":
            to_str += " (||)      "
        else:
            to_str += "      (||) "
        to_str += "(%d, %d)" % (self.miss[1], self.cann[1])
        return to_str

    def __eq__(self, other):
        return self.miss == other.miss and self.cann == other.cann and self.boat_position == other.boat_position

    def succ(self, action):

        direccion = action[0]
        misioneros_viajando = int (action[1])
        canibales_viajando = int (action[2])
        misioneros_izquierda = int (self.miss[0])
        canibales_izquierda = int (self.cann[0])
        misioneros_derecha = int (self.miss[1])
        canibales_derecha = int (self.cann[1])
        posicion_barco = self.boat_position
        
        if direccion == '>' and posicion_barco == 'left':
            canibales_derecha = canibales_derecha + canibales_viajando
            misioneros_derecha = misioneros_derecha + misioneros_viajando
            canibales_izquierda = canibales_izquierda - canibales_viajando
            misioneros_izquierda = misioneros_izquierda - misioneros_viajando
            posicion_barco = 'right'
        
        elif direccion == '<' and posicion_barco == 'right':
            canibales_derecha = canibales_derecha - canibales_viajando
            misioneros_derecha = misioneros_derecha - misioneros_viajando
            canibales_izquierda = canibales_izquierda + canibales_viajando
            misioneros_izquierda = misioneros_izquierda + misioneros_viajando
            posicion_barco = "left"
        
        else:
            return None
        
        if canibales_derecha > misioneros_derecha and misioneros_derecha > 0:
            return None
        
        if canibales_izquierda > misioneros_izquierda and misioneros_izquierda > 0:
            return None
        
        if canibales_izquierda < 0 or misioneros_izquierda <0 or canibales_derecha < 0 or misioneros_derecha < 0:
            return None
        
        return MissionariesState(misioneros_izquierda, canibales_izquierda, misioneros_derecha, canibales_derecha, posicion_barco,self.capacity)

    def next_states(self):
        new_states = []
        movimientos_izquierda = ['>01', '>10', '>11', '>02', '>20']
        movimientos_derecha = ['<01', '<10', '<11', '<02', '<20']
        action = None
        if self.boat_position == 'right':
            #si el barco esta en la orilla derecha, moveremos hacia la izquierda
            action = movimientos_derecha
        else:
            action = movimientos_izquierda
        
        for i in range(len(action)):
            estado = self.succ(action[i])
            if estado != None:
                new_states.append([estado, action[i]])
        
        return new_states    
