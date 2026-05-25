import unittest

from frontend.lib import api, ui


class UiTests(unittest.TestCase):
    def test_friendly_error_maps_known_http_statuses(self):
        cases = [
            (0, "API offline em http://localhost:8000", "API offline"),
            (400, "Agendamento deve ser no futuro", "Revise os dados"),
            (401, "Token invalido", "Sessao expirada"),
            (403, "Sem permissao", "Acesso restrito"),
            (404, "Nao encontrado", "Registro nao encontrado"),
            (409, "Faixa sobrepoe outra", "Conflito"),
            (500, "Internal Server Error", "Erro interno"),
        ]

        for status_code, detail, expected in cases:
            with self.subTest(status_code=status_code):
                message = ui.friendly_error(api.ApiError(status_code, detail))
                self.assertIn(expected, message)
                self.assertNotIn("Internal Server Error", message)

    def test_friendly_error_preserves_useful_detail_for_validation_errors(self):
        message = ui.friendly_error(api.ApiError(400, "Horario indisponivel para o profissional"))

        self.assertIn("Revise os dados", message)
        self.assertIn("Horario indisponivel para o profissional", message)


if __name__ == "__main__":
    unittest.main()
