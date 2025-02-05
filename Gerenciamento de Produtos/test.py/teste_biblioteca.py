from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import sqlite3


class RegistroProduto(BoxLayout):
    def limpar_campos(self):
        self.ids.entrada_id.text = ""
        self.ids.entrada_nome.text = ""
        self.ids.entrada_quantidade.text = ""
        self.ids.entrada_data.text = ""

    def salvar_produto(self):
        id_produto = self.ids.entrada_id.text
        nome_produto = self.ids.entrada_nome.text
        quantidade = self.ids.entrada_quantidade.text
        data_vencimento = self.ids.entrada_data.text

        if not id_produto or not nome_produto or not quantidade or not data_vencimento:
            self.mostrar_popup("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            banco_principal = sqlite3.connect("banco.db")
            cursor = banco_principal.cursor()
            cursor.execute(
                "INSERT INTO estoque (IDproduto, NOMEproduto, QUANTIDADEproduto, DATAVENCIMENTOproduto) VALUES (?, ?, ?, ?)",
                (id_produto, nome_produto, quantidade, data_vencimento)
            )
            banco_principal.commit()
            banco_principal.close()
            self.mostrar_popup("Sucesso", "Produto registrado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao registrar produto: {e}")

    def mostrar_popup(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.8, 0.5),
            auto_dismiss=True,
        )
        popup.open()


class RegistroApp(App):
    def build(self):
        return RegistroProduto()


if __name__ == "__main__":
    RegistroApp().run()
