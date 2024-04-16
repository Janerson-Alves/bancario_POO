# Importação de bibliotecas necessárias
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Classe Cliente que armazena informações e métodos relacionados a um cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco  # Armazena o endereço do cliente
        self.contas = []  # Lista de contas bancárias associadas ao cliente

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)  # Executa uma transação na conta especificada

    def adicionar_conta(self, conta):
        self.contas.append(conta)  # Adiciona uma nova conta à lista de contas do cliente

# Subclasse de Cliente para clientes que são pessoas físicas
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)  # Inicializa a classe base com o endereço
        self.nome = nome  # Nome da pessoa
        self.data_nascimento = data_nascimento  # Data de nascimento
        self.cpf = cpf  # CPF (Cadastro de Pessoa Física)

# Classe Conta que representa uma conta bancária genérica
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0  # Saldo inicial da conta
        self._numero = numero  # Número da conta
        self._agencia = "0001"  # Agência padrão
        self._cliente = cliente  # Cliente dono da conta
        self._historico = Historico()  # Histórico de transações

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)  # Método de classe para criar uma nova conta

    # Métodos getter para acessar os atributos privados
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

    # Métodos para realizar operações de saque e depósito
    def sacar(self, valor):
        # Verifica se o valor solicitado está disponível e é válido
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

# ContaCorrente é uma especialização de Conta com limites específicos
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite  # Limite de saque por operação
        self._limite_saques = limite_saques  # Limite de saques permitidos

    # Sobrescreve o método de saque para adicionar verificação de limites
    def sacar(self, valor):
        # Conta saques já realizados
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        # Retorna uma representação em string da conta corrente
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Histórico, que armazena as transações realizadas em uma conta
class Historico:
    def __init__(self):
        self._transacoes = []  # Lista de transações

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # Adiciona uma nova transação ao histórico
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

# Classe abstrata para transações
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Classes concretas para tipos específicos de transações, como Saque e Depósito
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Funções para manipulação e interação com o usuário
def menu():
    # Mostra o menu de opções para o usuário e captura a escolha
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    # Filtra os clientes pelo CPF e retorna o cliente correspondente
    for cliente in clientes:
        if hasattr(cliente, "cpf") and cliente.cpf == cpf:
            return cliente
    return None

# Função para criar uma nova conta para um cliente
def criar_nova_conta(clientes):
    cpf_cliente = input("\nDigite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf_cliente, clientes)
    if cliente:
        nova_conta = ContaCorrente(input("Informe o número da conta: "), cliente)
        cliente.adicionar_conta(nova_conta)
        print("\n=== Nova conta criada com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! Cliente não encontrado. @@@")

# Função para depositar um valor em uma conta específica
def realizar_deposito(cliente):
    num_conta = input("\nDigite o número da conta: ")
    conta = next((acc for acc in cliente.contas if acc.numero == num_conta), None)
    if conta:
        valor = float(input("Digite o valor a ser depositado: "))
        deposito = Deposito(valor)
        cliente.realizar_transacao(conta, deposito)
    else:
        print("\n@@@ Operação falhou! Conta não encontrada. @@@")
