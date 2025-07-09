import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime, UTC
from pathlib import Path

ROOT_PATH = Path(__file__).parent

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite, limite_saques):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        saques_hoje = [t for t in self.historico.transacoes if t["tipo"] == "Saque"]
        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif len(saques_hoje) >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        return False

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now(UTC).strftime("%d-%m-%Y %H:%M:%S")
        })

    def transacoes_do_dia(self):
        hoje = datetime.now(UTC).date()
        return [t for t in self._transacoes if datetime.strptime(t["data"], "%d-%m-%Y %H:%M:%S").date() == hoje]

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self): pass

    @abstractclassmethod
    def registrar(self, conta): pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def log_transacao(func):
    def wrapper(*args, **kwargs):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ROOT_PATH / "log.txt", "a") as f:
            f.write(f"[{data_hora}] Função '{func.__name__}' executada.\n")
        return func(*args, **kwargs)
    return wrapper

def filtrar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta: return
    cliente.realizar_transacao(conta, transacao)

    with open(ROOT_PATH / "log.txt", "a") as f:
        f.write(f"Depósito registrado: R$ {valor:.2f}\n")

@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta: return
    cliente.realizar_transacao(conta, transacao)

    with open(ROOT_PATH / "log.txt", "a") as f:
        f.write(f"Saque registrado: R$ {valor:.2f}\n")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")

    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Cliente já existe! @@@")
        return

    nome = input("Informe o nome completo: ").title()
    nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    clientes.append(PessoaFisica(nome, nasc, cpf, endereco))
    print("\n=== Cliente criado com sucesso! ===")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    conta = ContaCorrente.nova_conta(cliente, numero_conta, 500, 3)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

@log_transacao
def exibir_extrato(clientes):
    cpf = input("CPF: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta: return

    print("\n================ EXTRATO ================")
    for t in conta.historico.transacoes:
        print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("========================================")

def menu():
    return input(textwrap.dedent("""
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo cliente
    [q] Sair
    => """))

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 50)
        print(textwrap.dedent(str(conta)))

def main():
    clientes, contas = [], []
    while True:
        opcao = menu()
        if opcao == "d": depositar(clientes)
        elif opcao == "s": sacar(clientes)
        elif opcao == "e": exibir_extrato(clientes)
        elif opcao == "nu": criar_cliente(clientes)
        elif opcao == "nc": criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "lc": listar_contas(contas)
        elif opcao == "q": break
        else: print("\n@@@ Opção inválida! @@@")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n=== Programa finalizado pelo usuário. ===")
