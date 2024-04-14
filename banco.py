from abc import ABC, abstractmethod

#Criando a classe historico
class Historico:
    def __init__(self):
        self._historico  = []
    
    #Criando função para adicionar a transação a lista historico 
    def adicionarTransacao(self, transacao):
        self._historico.append(transacao)

#Criando a classe Transação
class Transacao(ABC):
    #Criando uma função abstrata(todos que herdar de Transação dele deverá ter essa função)
    @abstractmethod
    def registrar(self, saldo):
        pass

#Criando a classe Transação 
class Deposito(Transacao):
    #Registrando o deposito
    def registrar(self, saldo, conta):
        conta.adicionarTransacao(f'Deposito de R$ {saldo:.2f}')
        conta.depositar(saldo)

#Criando a classe Saque
class Saque(Transacao):
    #registrando o saque
    def registar(self, saldo, conta):
        if saldo.saque(conta):
            conta.adicionarTransacao(f'Saque de R$ {saldo:.2f}')
        else:
            print('Saldo Insuficiente para Saque!')

#Criando classe conta
class Conta(ABC):
    def __init__(self, numero_conta, cliente, agencia):
        #Instancias da classe
        self._saldo = 0
        self._numero_conta = numero_conta
        self._cliente = cliente     
        self._agencia = agencia   
        self._historio = Historico()
    
    #metodos abstratos
    @abstractmethod
    def criar_conta(self):
        pass
    
    
    @abstractmethod
    def sacar(self):
        pass
    
    @abstractmethod
    def depositar(self):
        pass
    
    #metodos de propriedades abstratas
    @property
    @abstractmethod
    def saldo(self):
        pass
    
    @property
    @abstractmethod
    def numero_conta(self):
        pass
    
    def verifica_saldo(self):
        return self._saldo
    
#criando classe contaConrrente    
class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, agencia, limite, limite_saque):
        #herdando da classe Conta
        super().__init__(numero_conta, cliente, agencia)
        #Instancias da classe
        self._limite = limite
        self._limite_saque = limite_saque
        
    def criar_conta(self):
        self._numero_conta
        
        
    def saldo(self):
        # Considera o limite na verificação do saldo
        return f'Saldo atual: R$ {self._saldo:.2f}'
    
    def numero_conta(self):
        return self._numero_conta
    
    #Implementa o deposito no valor e retorna uma mensagem
    def depositar(self, valor):
        self._saldo += valor
        return f'Deposito de R$ {valor:.2f} Realizado com sucesso!'
    
    #Implementa o sacar no valor e retorna uma mensagem
    def sacar(self, valor):
        if self._saldo + self._limite >= valor and self._limite_saque > 0:
            self._saldo -= valor
            self._limite_saque =- 1
            return f'Saque de R$ {valor:.2f} Realizado com sucesso!'
    
    #retorna as informações da conta    
    def __str__(self):
        return f'Informações da Conta Corrente / Cliente: {self._cliente} | Agencia: {self._agencia} Conta Corrente Nª: {self._numero_conta} | Limite: {self._limite} | Limite de Saque: {self._limite_saque}'
        
#Crianco classe Cliente (ABSTRATA)
class Cliente(ABC):
    def __init__(self, endereco):
        #instancias da classe
        self._endereco = endereco
        self._contas = []
    
    #Metodos abstratos    
    @abstractmethod
    def realizar_transacao(self, transacao):
        pass
    #Propriedades abstradas
    @property
    @abstractmethod
    def endereco(self):
        pass
    
    @property
    @abstractmethod
    def contas(self):
        pass
    
    #Adiciona a conta a lista de contas
    def adicionar_conta(self, conta):
        self._contas.append(conta)

#Criando classe pessoa fisica        
class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        #Herdando da classe Cliente
        super().__init__(endereco)
        #Instancias da classe
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        
    #Adiciona a transação na lista de contas
    def realizar_transacao(self, transacao):
        self._contas.append(transacao)
    
    #Propriedades para retornar valores   
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas
    
    #Retorna uma mensagem com as informações da conta
    def __str__(self):
        return f'Informações da pessoa fisica / Nome: {self._nome} | CPF: {self._cpf} | Endereço: {self._endereco} | Data de Nascimento: {self._data_nascimento}'
    
    
#criando instancia de pessoa fisica
p1 = PessoaFisica('Rua x 123', '123456', 'Carlos', '15/03/1998')
print(p1)

#Criando conta corrente para Pessoa Fisica            
cc1 = ContaCorrente('12345', p1, 1, 1000, 5)
print(cc1)

#testando metodos depositar, sacar e saldo
print(cc1.depositar(500))
print(cc1.sacar(200))
print(cc1.saldo())
            
    

            
    


