$(document).ready(function(){
  if(window.location.hash)
  {
    var hash = window.location.hash.substring(1);
    if(hash=='signup')
    {
      document.getElementById('signupTabButton').click();
    }
    else
    {
      document.getElementById('signupTabButton').click();
      window.setTimeout(function(){document.getElementById('loginTabButton').click();}, 150);
    }
  }
  else
  {
    document.getElementById('signupTabButton').click();
    window.setTimeout(function(){document.getElementById('loginTabButton').click();}, 150);
  }
});
