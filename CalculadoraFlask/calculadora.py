from flask import request, render_template

def calcular():
    operacao = request.form.get('operacao', '+')

    if operacao in ['+', '-', '*', '/', '**', 'sqrt']:
        num1_valor = request.form.get("num1", "").strip()
        num2_valor = request.form.get("num2", "").strip()

        if not num1_valor:
            return render_template("calculadora.html", etapas="Informe o primeiro número.", resultados="")

        num1 = float(num1_valor)

        if operacao == "sqrt":
          resultado = num1 ** 0.5
          etapas = f"√{num1} = {resultado:.4f}"
        else:
            if not num2_valor:
                return render_template("calculadora.html", etapas="Informe o segundo número para esta operação.", resultados="")
            num2 = float(num2_valor)

            if operacao == "+":
               resultado = num1 + num2
               etapas = f"{num1} + {num2} = {resultado}"
            elif operacao == "-":
                 resultado = num1 - num2
                 etapas = f"{num1} - {num2} = {resultado}"
            elif operacao == "*":
                 resultado = num1 * num2
                 etapas = f"{num1} × {num2} = {resultado}"
            elif operacao == "/":
                if num2 == 0:
                   resultado = "Erro: Divisão por zero"
                   etapas = "Não é possível dividir por zero."
                else:
                   resultado = num1 / num2
                   etapas = f"{num1} / {num2} = {resultado:.4f}"
            elif operacao == "**":
                resultado = num1 ** num2
                etapas = f"{num1} ** {num2} = {resultado}"

    elif operacao == "bhaskara":
        a = float(request.form.get("a", 0))
        b = float(request.form.get("b", 0))
        c = float(request.form.get("c", 0))

        if a == 0:
            return render_template("calculadora.html", etapas="Erro: a não pode ser zero.", resultados="")

        delta = b**2 - 4*a*c
        etapas = f"Δ = {delta:.2f}"

        if delta > 0:
            x1 = (-b + delta**0.5) / (2*a)
            x2 = (-b - delta**0.5) / (2*a)
            resultados = f"x₁ = {x1:.4f}<br>x₂ = {x2:.4f}"
        elif delta == 0:
            x = -b / (2*a)
            resultados = f"x = {x:.4f} (raiz dupla)"
        else:
           real = -b / (2*a)
           imag = (abs(delta)**0.5) / (2*a)
           resultados = f"{real:.4f} ± {imag:.4f}i"

    else:
       resultado = "Operação inválida"
       etapas = "A operação selecionada é inválida."

    return render_template("calculadora.html", etapas=etapas, resultados=resultados)