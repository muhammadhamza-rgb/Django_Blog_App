// Function to set or replace placeholder
function setPlaceholder(inputId, text) {
  const el = document.getElementById(inputId);
  if (el) {
    el.placeholder = text; // will set new or overwrite existing
  }
}

// Example usage
setPlaceholder("id_title", "Enter title here");
setPlaceholder("id_category", "Select category");
setPlaceholder("id_content", "Write your post...");
setPlaceholder("id_username", "Enter username");
setPlaceholder("id_password", "Enter your password");
setPlaceholder("id_email", "abc@123.com");
setPlaceholder("id_password1", "Enter a strong passsword");
setPlaceholder("id_password2", "Enter the password again");
