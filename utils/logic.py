# -*- coding: utf-8 -*-

def calculate_logic(data):
    try:
        operation = data.get('operation', '').lower()
        a_raw = data.get('a', '')
        b_raw = data.get('b', None)

        def parse_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, int):
                return bool(val)
            s = str(val).strip().lower()
            if s in ('1', 'true', 'yes'):
                return True
            if s in ('0', 'false', 'no'):
                return False
            raise ValueError('Nilai tidak valid: {}'.format(val))

        if a_raw == '' or a_raw is None:
            return {'success': False, 'error': 'INPUT A TIDAK BOLEH KOSONG'}

        try:
            a = parse_bool(a_raw)
        except ValueError:
            return {'success': False, 'error': 'INPUT A HARUS 0 ATAU 1'}

        if operation != 'not':
            if b_raw == '' or b_raw is None:
                return {'success': False, 'error': 'INPUT B TIDAK BOLEH KOSONG'}
            try:
                b = parse_bool(b_raw)
            except ValueError:
                return {'success': False, 'error': 'INPUT B HARUS 0 ATAU 1'}
        else:
            b = None

        result = None
        formula = ''
        steps = []
        truth_table = []

        a_int = 1 if a else 0
        b_int = (1 if b else 0) if b is not None else None

        if operation == 'and':
            result = a and b
            formula = '{} AND {} = {}'.format(a_int, b_int, 1 if result else 0)
            steps = [
                'OPERASI: AND (DAN LOGIKA)',
                'DEFINISI: True hanya jika KEDUA input True',
                'INPUT A: {} ({})'.format(a_int, 'TRUE' if a else 'FALSE'),
                'INPUT B: {} ({})'.format(b_int, 'TRUE' if b else 'FALSE'),
                'HASIL: {} AND {} = {}'.format(a_int, b_int, 1 if result else 0)
            ]
            truth_table = [
                {'a': 0, 'b': 0, 'result': 0},
                {'a': 0, 'b': 1, 'result': 0},
                {'a': 1, 'b': 0, 'result': 0},
                {'a': 1, 'b': 1, 'result': 1},
            ]

        elif operation == 'or':
            result = a or b
            formula = '{} OR {} = {}'.format(a_int, b_int, 1 if result else 0)
            steps = [
                'OPERASI: OR (ATAU LOGIKA)',
                'DEFINISI: True jika SALAH SATU input True',
                'INPUT A: {} ({})'.format(a_int, 'TRUE' if a else 'FALSE'),
                'INPUT B: {} ({})'.format(b_int, 'TRUE' if b else 'FALSE'),
                'HASIL: {} OR {} = {}'.format(a_int, b_int, 1 if result else 0)
            ]
            truth_table = [
                {'a': 0, 'b': 0, 'result': 0},
                {'a': 0, 'b': 1, 'result': 1},
                {'a': 1, 'b': 0, 'result': 1},
                {'a': 1, 'b': 1, 'result': 1},
            ]

        elif operation == 'not':
            result = not a
            formula = 'NOT {} = {}'.format(a_int, 1 if result else 0)
            steps = [
                'OPERASI: NOT (NEGASI)',
                'DEFINISI: Membalik nilai input',
                'INPUT A: {} ({})'.format(a_int, 'TRUE' if a else 'FALSE'),
                'HASIL: NOT {} = {}'.format(a_int, 1 if result else 0)
            ]
            truth_table = [
                {'a': 0, 'result': 1},
                {'a': 1, 'result': 0},
            ]

        elif operation == 'xor':
            result = a ^ b
            formula = '{} XOR {} = {}'.format(a_int, b_int, 1 if result else 0)
            steps = [
                'OPERASI: XOR (EKSKLUSIF ATAU)',
                'DEFINISI: True jika TEPAT SATU input True',
                'INPUT A: {} ({})'.format(a_int, 'TRUE' if a else 'FALSE'),
                'INPUT B: {} ({})'.format(b_int, 'TRUE' if b else 'FALSE'),
                'HASIL: {} XOR {} = {}'.format(a_int, b_int, 1 if result else 0)
            ]
            truth_table = [
                {'a': 0, 'b': 0, 'result': 0},
                {'a': 0, 'b': 1, 'result': 1},
                {'a': 1, 'b': 0, 'result': 1},
                {'a': 1, 'b': 1, 'result': 0},
            ]

        elif operation == 'nand':
            result = not (a and b)
            formula = '{} NAND {} = {}'.format(a_int, b_int, 1 if result else 0)
            steps = [
                'OPERASI: NAND (NOT AND)',
                'DEFINISI: Kebalikan dari AND',
                'LANGKAH 1: {} AND {} = {}'.format(a_int, b_int, 1 if (a and b) else 0),
                'LANGKAH 2: NOT {} = {}'.format(1 if (a and b) else 0, 1 if result else 0),
                'HASIL: {} NAND {} = {}'.format(a_int, b_int, 1 if result else 0)
            ]
            truth_table = [
                {'a': 0, 'b': 0, 'result': 1},
                {'a': 0, 'b': 1, 'result': 1},
                {'a': 1, 'b': 0, 'result': 1},
                {'a': 1, 'b': 1, 'result': 0},
            ]

        elif operation == 'nor':
            result = not (a or b)
            formula = '{} NOR {} = {}'.format(a_int, b_int, 1 if result else 0)
            steps = [
                'OPERASI: NOR (NOT OR)',
                'DEFINISI: Kebalikan dari OR',
                'LANGKAH 1: {} OR {} = {}'.format(a_int, b_int, 1 if (a or b) else 0),
                'LANGKAH 2: NOT {} = {}'.format(1 if (a or b) else 0, 1 if result else 0),
                'HASIL: {} NOR {} = {}'.format(a_int, b_int, 1 if result else 0)
            ]
            truth_table = [
                {'a': 0, 'b': 0, 'result': 1},
                {'a': 0, 'b': 1, 'result': 0},
                {'a': 1, 'b': 0, 'result': 0},
                {'a': 1, 'b': 1, 'result': 0},
            ]

        else:
            return {'success': False, 'error': 'OPERASI TIDAK DIKENAL: {}'.format(operation)}

        result_display = 'TRUE (1)' if result else 'FALSE (0)'

        return {
            'success': True,
            'result': result_display,
            'result_bool': bool(result),
            'formula': formula,
            'steps': steps,
            'truth_table': truth_table,
            'operation': operation.upper()
        }

    except Exception as e:
        return {'success': False, 'error': 'TERJADI KESALAHAN: {}'.format(str(e))}
