const passwordInput = document.getElementById('password'); 
const toggleCheckbox= document.getElementById('togglePassword'); 
toggleCheckbox.addEventListener('change',() =>{
    passwordInput.type = toggleCheckbox.checked ? 'text' : 'password';
}); 
