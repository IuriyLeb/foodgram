import io

from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

from recipes.models import Recipe, RecipeIngredient


def process_shopping_cart(shopping_cart_set):
    """
    Get queryset of all user's shopping cart objects.
    Returns dictionary for render.
    """
    ingredients_dict = {}

    for shopping_cart in shopping_cart_set:
        recipe = Recipe.objects.get(id=shopping_cart.recipe.id)
        recipes_set = RecipeIngredient.objects.filter(recipe=recipe)
        for recipe in recipes_set:
            ingr_name = recipe.ingredient.name
            if ingr_name not in ingredients_dict.keys():
                ingredients_dict[ingr_name] = [
                    recipe.amount,
                    recipe.ingredient.measurement_unit
                ]
            else:
                ingredients_dict[ingr_name][0] += recipe.amount
    return ingredients_dict


def render_pdf(ingredients):
    """
    Get ingredients dictionary({ingredient_name: [amount, measurement_unit]}).
    Returns rendered pdf file.
    """
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer, pagesize=A5)
    x, y = 30, 550
    pdf_file.setFont('VC', 14)
    textobject = pdf_file.beginText(x, y)

    for ingredient, quantity in ingredients.items():
        result_string = (
            ingredient
            + f' ({quantity[1]})'
            + ' -- '
            + f'{quantity[0]}'
        )

        textobject.textLine(result_string)

    pdf_file.drawText(textobject)
    pdf_file.showPage()
    pdf_file.save()
    buffer.seek(0)
    return buffer
