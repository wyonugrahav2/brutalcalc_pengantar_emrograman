# -*- coding: utf-8 -*-
import math

def calculate_arithmetic(data):
    try:
        operation = data.get('operation', '').lower()
        a_raw = data.get('a', '')
        b_raw = data.get('b', '')

        if a_raw == '' or a_raw is None:
            return {'success': False, 'error': 'INPUT A TIDAK BOLEH KOSONG'}

        try:
            a = float(a_raw)
        except (ValueError, TypeError):
            return {'success': False, 'error': 'INPUT A HARUS BERUPA ANGKA'}

        if operation != 'sqrt':
            if b_raw == '' or b_raw is None:
                return {'success': False, 'error': 'INPUT B TIDAK BOLEH KOSONG'}
            try:
                b = float(b_raw)
            except (ValueError, TypeError):
                return {'success': False, 'error': 'INPUT B HARUS BERUPA ANGKA'}
        else:
            b = None

        result = None
        formula = ''
        steps = []

        if operation == 'add':
            result = a + b
            formula = '{} + {} = {}'.format(a, b, result)
            steps = [
                'OPERASI: PENJUMLAHAN',
                'RUMUS: A + B',
                'SUBSTITUSI: {} + {}'.format(a, b),
                'HASIL: {}'.format(result)
            ]

        elif operation == 'subtract':
            result = a - b
            formula = '{} - {} = {}'.format(a, b, result)
            steps = [
                'OPERASI: PENGURANGAN',
                'RUMUS: A - B',
                'SUBSTITUSI: {} - {}'.format(a, b),
                'HASIL: {}'.format(result)
            ]

        elif operation == 'multiply':
            result = a * b
            formula = '{} x {} = {}'.format(a, b, result)
            steps = [
                'OPERASI: PERKALIAN',
                'RUMUS: A x B',
                'SUBSTITUSI: {} x {}'.format(a, b),
                'HASIL: {}'.format(result)
            ]

        elif operation == 'divide':
            if b == 0:
                return {'success': False, 'error': 'PEMBAGIAN DENGAN NOL TIDAK DIIZINKAN'}
            result = a / b
            formula = '{} / {} = {}'.format(a, b, round(result, 6))
            steps = [
                'OPERASI: PEMBAGIAN',
                'RUMUS: A / B',
                'SUBSTITUSI: {} / {}'.format(a, b),
                'VERIFIKASI: B != 0 (VALID)',
                'HASIL: {}'.format(round(result, 6))
            ]

        elif operation == 'modulus':
            if b == 0:
                return {'success': False, 'error': 'MODULUS DENGAN NOL TIDAK DIIZINKAN'}
            result = a % b
            formula = '{} % {} = {}'.format(a, b, result)
            steps = [
                'OPERASI: MODULUS (SISA BAGI)',
                'RUMUS: A % B',
                'SUBSTITUSI: {} % {}'.format(a, b),
                'PENJELASAN: {} dibagi {} = {} sisa {}'.format(a, b, int(a // b), result),
                'HASIL: {}'.format(result)
            ]

        elif operation == 'floor_division':
            if b == 0:
                return {'success': False, 'error': 'FLOOR DIVISION DENGAN NOL TIDAK DIIZINKAN'}
            result = int(a // b)
            formula = '{} // {} = {}'.format(a, b, result)
            steps = [
                'OPERASI: FLOOR DIVISION (PEMBAGIAN BULAT)',
                'RUMUS: A // B',
                'SUBSTITUSI: {} // {}'.format(a, b),
                'PENJELASAN: {} / {} = {} (dibulatkan ke bawah)'.format(a, b, a / b),
                'HASIL: {}'.format(result)
            ]

        elif operation == 'power':
            result = a ** b
            formula = '{} ^ {} = {}'.format(a, b, result)
            steps = [
                'OPERASI: PERPANGKATAN',
                'RUMUS: A ^ B',
                'SUBSTITUSI: {} ^ {}'.format(a, b),
                'PENJELASAN: {} dipangkatkan {}'.format(a, b),
                'HASIL: {}'.format(result)
            ]

        elif operation == 'sqrt':
            if a < 0:
                return {'success': False, 'error': 'AKAR KUADRAT BILANGAN NEGATIF TIDAK VALID'}
            result = round(math.sqrt(a), 6)
            formula = 'sqrt({}) = {}'.format(a, result)
            steps = [
                'OPERASI: AKAR KUADRAT',
                'RUMUS: sqrt(A)',
                'SUBSTITUSI: sqrt({})'.format(a),
                'PENJELASAN: Mencari nilai x dimana x^2 = {}'.format(a),
                'HASIL: {}'.format(result)
            ]

        else:
            return {'success': False, 'error': 'OPERASI TIDAK DIKENAL: {}'.format(operation)}

        # Format result nicely
        if isinstance(result, float) and result == int(result):
            result_display = int(result)
        else:
            result_display = round(result, 6) if isinstance(result, float) else result

        return {
            'success': True,
            'result': result_display,
            'formula': formula,
            'steps': steps
        }

    except Exception as e:
        return {'success': False, 'error': 'TERJADI KESALAHAN: {}'.format(str(e))}
