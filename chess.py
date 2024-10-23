from chess_board import Board

def test_en_passant_select():
    b = Board()

    b.move('E2', 'E4')
    b.move('A7', 'A5')
    b.move('E4', 'E5')
    b.move('F7', 'F5')

    return b.select('E5') == ['E6', 'F6']

def test_castling_short_select():
    b = Board()

    b.move('E2', 'E3')
    b.move('E7', 'E6')

    b.move('G1', 'F3')
    b.move('F7', 'F6')

    b.move('F1', 'E2')
    b.move('G7', 'G6')

    return b.select('E1') == ['F1', 'H1']

def test_castling_short_move():
    b = Board()

    b.move('E2', 'E3')
    b.move('E7', 'E6')

    b.move('G1', 'F3')
    b.move('F7', 'F6')

    b.move('F1', 'E2')
    b.move('G7', 'G6')

    b.move('E1', 'H1')
    b.move('H7', 'H6')

    return b.select('G1') == ['H1']

if __name__ == '__main__':
    # r = test_en_passant_select()
    # print(r)

    r = test_castling_short_move()
    print(r)
