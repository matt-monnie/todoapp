document.getElementById('dark-mode-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
});

// Set intitial dark mode statse based on preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Toggle Recipe Form Visibility
document.getElementById('toggle-form').addEventListener('click', function() {
    var form = document.getElementById('recipe-form');
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
});

// Add ingredient fields dynamically
document.getElementById('add-ingredient').addEventListener('click', function() {
    var ingredientsSection = document.getElementById('ingredients-section');
    var newIngredient = document.createElement('div');
    newIngredient.classList.add('ingredient');
    newIngredient.innerHTML = `
        <input type="text" name="ingredient_quantity[]" placeholder="Quantity" required>
        <select name="ingredient_unit[]">
            <option value="g">g</option>
            <option value="ml">ml</option>
            <option value="oz">oz</option>
            <option value="tsp">tsp</option>
            <option value="tbsp">tbsp</option>
            <option value="cup">cup</option>
            <!-- Add more units as needed -->
        </select>
        <input type="text" name="ingredient_name[]" placeholder="Ingredient" required>
    `;
    ingredientsSection.appendChild(newIngredient);
});

// Display Recipe Details
document.querySelectorAll('.recipe-list a').forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        var recipeId = this.getAttribute('href').split('/').pop();

        fetch(`/recipes/${recipeId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('recipe-title').innerText = data.name;
                var ingredientsList = document.getElementById('ingredients-list');
                ingredientsList.innerHTML = '';
                data.ingredients.forEach(function(ingredient) {
                    var li = document.createElement('li');
                    li.innerText = `${ingredient.quantity} ${ingredient.unit} ${ingredient.name}`;
                    ingredientsList.appendChild(li);
                });
                document.getElementById('directions-text').innerText = data.directions;
                document.getElementById('recipe-details').style.display = 'block';
            });
    });
});

