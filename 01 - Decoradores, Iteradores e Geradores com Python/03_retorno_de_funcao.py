def calculadora(operacao):
    def somar(a, b):
        return a + b

    def subtrair(a, b):
        return a - b

    def multiplicacao(a, b):
        return a * b

    def divisao(a, b):
        return a / b

    ## Match é semelhante ao switch case
    match operacao:
        case "+":
            return somar
        case "-":
            return subtrair
        case "*":
            return multiplicacao
        case "/":
            return divisao
        case _:
            return "Operação inválida!"


op = calculadora("+")
print(f"Resultado: {op(2, 2)}")

op = calculadora("-")
print(f"Resultado: {op(2, 2)}")

op = calculadora("*")
print(f"Resultado: {op(2, 2)}")

op = calculadora("/")
print(f"Resultado: {round(op(2, 2), 2)}")
