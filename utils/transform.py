# -*- coding: utf-8 -*-
import math

# Static currency rates (base: IDR)
CURRENCY_RATES = {
    'IDR': 1,
    'USD': 0.000062,
    'EUR': 0.000057,
    'SGD': 0.000083,
    'JPY': 0.0094,
    'MYR': 0.000290,
    'GBP': 0.000049,
    'AUD': 0.000096,
}

def calculate_transform(data):
    try:
        t = data.get('type', '').lower()

        if t == 'base':
            return _base_convert(data)
        elif t == 'temperature':
            return _temperature_convert(data)
        elif t == 'currency':
            return _currency_convert(data)
        elif t == 'factorial':
            return _factorial(data)
        elif t == 'fibonacci':
            return _fibonacci(data)
        else:
            return {'success': False, 'error': 'TIPE TRANSFORM TIDAK DIKENAL'}

    except Exception as e:
        return {'success': False, 'error': 'TERJADI KESALAHAN: {}'.format(str(e))}


def _base_convert(data):
    val_raw = data.get('value', '')
    from_base = data.get('from_base', 'decimal').lower()
    to_base = data.get('to_base', 'binary').lower()

    if val_raw == '':
        return {'success': False, 'error': 'INPUT NILAI TIDAK BOLEH KOSONG'}

    base_map = {'decimal': 10, 'binary': 2, 'octal': 8, 'hexadecimal': 16}

    if from_base not in base_map:
        return {'success': False, 'error': 'BASIS ASAL TIDAK VALID'}
    if to_base not in base_map:
        return {'success': False, 'error': 'BASIS TUJUAN TIDAK VALID'}

    try:
        decimal_val = int(str(val_raw), base_map[from_base])
    except ValueError:
        return {'success': False, 'error': 'NILAI TIDAK VALID UNTUK BASIS {}'.format(from_base.upper())}

    if to_base == 'decimal':
        result = str(decimal_val)
    elif to_base == 'binary':
        result = bin(decimal_val)[2:]
    elif to_base == 'octal':
        result = oct(decimal_val)[2:]
    elif to_base == 'hexadecimal':
        result = hex(decimal_val)[2:].upper()

    formula = '{} ({}) = {} ({})'.format(val_raw, from_base.upper(), result, to_base.upper())

    steps = [
        'OPERASI: KONVERSI BASIS BILANGAN',
        'INPUT: {} (BASIS {})'.format(val_raw, base_map[from_base]),
        'KONVERSI KE DESIMAL: {}'.format(decimal_val),
        'KONVERSI KE BASIS {}: {}'.format(base_map[to_base], result),
        'HASIL AKHIR: {}'.format(result)
    ]

    return {
        'success': True,
        'result': result,
        'formula': formula,
        'steps': steps
    }


def _temperature_convert(data):
    val_raw = data.get('value', '')
    from_unit = data.get('from_unit', '').lower()
    to_unit = data.get('to_unit', '').lower()

    if val_raw == '':
        return {'success': False, 'error': 'INPUT NILAI TIDAK BOLEH KOSONG'}

    try:
        val = float(val_raw)
    except (ValueError, TypeError):
        return {'success': False, 'error': 'NILAI HARUS BERUPA ANGKA'}

    units = ['celsius', 'fahrenheit', 'kelvin', 'reamur']
    if from_unit not in units:
        return {'success': False, 'error': 'SATUAN ASAL TIDAK VALID'}
    if to_unit not in units:
        return {'success': False, 'error': 'SATUAN TUJUAN TIDAK VALID'}

    # Convert to Celsius first
    if from_unit == 'celsius':
        celsius = val
    elif from_unit == 'fahrenheit':
        celsius = (val - 32) * 5 / 9
    elif from_unit == 'kelvin':
        celsius = val - 273.15
    elif from_unit == 'reamur':
        celsius = val * 5 / 4

    # Convert from Celsius to target
    if to_unit == 'celsius':
        result = celsius
    elif to_unit == 'fahrenheit':
        result = (celsius * 9 / 5) + 32
    elif to_unit == 'kelvin':
        result = celsius + 273.15
    elif to_unit == 'reamur':
        result = celsius * 4 / 5

    result = round(result, 4)
    formula = '{} {} = {} {}'.format(val, from_unit.upper(), result, to_unit.upper())

    steps = [
        'OPERASI: KONVERSI SUHU',
        'INPUT: {} {}'.format(val, from_unit.upper()),
        'KONVERSI KE CELSIUS: {} C'.format(round(celsius, 4)),
        'KONVERSI KE {}: {}'.format(to_unit.upper(), result),
        'HASIL AKHIR: {} {}'.format(result, to_unit.upper())
    ]

    return {
        'success': True,
        'result': '{} {}'.format(result, to_unit.upper()),
        'formula': formula,
        'steps': steps
    }


def _currency_convert(data):
    val_raw = data.get('value', '')
    from_currency = data.get('from_currency', '').upper()
    to_currency = data.get('to_currency', '').upper()

    if val_raw == '':
        return {'success': False, 'error': 'INPUT NILAI TIDAK BOLEH KOSONG'}

    try:
        val = float(val_raw)
    except (ValueError, TypeError):
        return {'success': False, 'error': 'NILAI HARUS BERUPA ANGKA'}

    if val < 0:
        return {'success': False, 'error': 'NILAI TIDAK BOLEH NEGATIF'}

    if from_currency not in CURRENCY_RATES:
        return {'success': False, 'error': 'MATA UANG ASAL TIDAK VALID'}
    if to_currency not in CURRENCY_RATES:
        return {'success': False, 'error': 'MATA UANG TUJUAN TIDAK VALID'}

    val_in_idr = val / CURRENCY_RATES[from_currency]
    result = val_in_idr * CURRENCY_RATES[to_currency]
    result = round(result, 4)

    rate = CURRENCY_RATES[to_currency] / CURRENCY_RATES[from_currency]
    formula = '{} {} = {} {}'.format(val, from_currency, result, to_currency)

    steps = [
        'OPERASI: KONVERSI MATA UANG',
        'INPUT: {} {}'.format(val, from_currency),
        'RATE (STATIS): 1 {} = {} {}'.format(from_currency, round(rate, 6), to_currency),
        'KALKULASI: {} x {} = {}'.format(val, round(rate, 6), result),
        'HASIL AKHIR: {} {}'.format(result, to_currency),
        'CATATAN: RATE STATIS - BUKAN HARGA REAL-TIME'
    ]

    return {
        'success': True,
        'result': '{} {}'.format(result, to_currency),
        'formula': formula,
        'steps': steps
    }


def _factorial(data):
    val_raw = data.get('value', '')

    if val_raw == '':
        return {'success': False, 'error': 'INPUT NILAI TIDAK BOLEH KOSONG'}

    try:
        n = int(val_raw)
    except (ValueError, TypeError):
        return {'success': False, 'error': 'INPUT HARUS BILANGAN BULAT'}

    if n < 0:
        return {'success': False, 'error': 'FAKTORIAL TIDAK TERDEFINISI UNTUK BILANGAN NEGATIF'}
    if n > 20:
        return {'success': False, 'error': 'INPUT MAKSIMAL 20 (MENCEGAH OVERFLOW)'}

    result = math.factorial(n)

    # Build factorial notation
    if n == 0:
        notation = '0! = 1'
    else:
        parts = ' x '.join(str(i) for i in range(1, n + 1))
        notation = '{}! = {} = {}'.format(n, parts, result)

    steps = [
        'OPERASI: FAKTORIAL',
        'INPUT: {}!'.format(n),
        'RUMUS: n! = n x (n-1) x (n-2) x ... x 1',
        'EKSPANSI: {}'.format(' x '.join(str(i) for i in range(n, 0, -1)) if n > 0 else '1'),
        'HASIL AKHIR: {}'.format(result)
    ]

    return {
        'success': True,
        'result': str(result),
        'formula': notation,
        'steps': steps
    }


def _fibonacci(data):
    val_raw = data.get('value', '')

    if val_raw == '':
        return {'success': False, 'error': 'INPUT NILAI TIDAK BOLEH KOSONG'}

    try:
        n = int(val_raw)
    except (ValueError, TypeError):
        return {'success': False, 'error': 'INPUT HARUS BILANGAN BULAT'}

    if n < 1:
        return {'success': False, 'error': 'INPUT MINIMAL 1'}
    if n > 50:
        return {'success': False, 'error': 'INPUT MAKSIMAL 50'}

    fibs = [0, 1]
    for i in range(2, n + 1):
        fibs.append(fibs[-1] + fibs[-2])

    result_list = fibs[:n]
    result_str = ', '.join(str(x) for x in result_list)

    steps = [
        'OPERASI: DERET FIBONACCI',
        'INPUT: {} SUKU PERTAMA'.format(n),
        'RUMUS: F(n) = F(n-1) + F(n-2)',
        'F(1)=0, F(2)=1, dst...',
        'DERET: {}'.format(result_str)
    ]

    return {
        'success': True,
        'result': result_str,
        'formula': 'Fibonacci({}) = [{}]'.format(n, result_str),
        'steps': steps
    }
