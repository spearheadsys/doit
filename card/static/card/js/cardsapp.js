
// $(document).ready(function(){
  console.log("DoIT :: loading cardsapp.js")
  // do your thing here

  // todo, these do not work for our reply modals in editcard!!
  // if we navigate away with changes, let the user know
  var formSubmitting = false;
  var setFormSubmitting = function() { formSubmitting = true; };
  var unSetFormSubmitting = function() { formSubmitting = false; };
  window.addEventListener('beforeunload', function (e) {
    if (formSubmitting) {
      console.log('form submitting is true')
      return undefined;
    }
    // Cancel the event
    e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
    // Chrome requires returnValue to be set
    e.returnValue = '';
  });

  // make sure we unload before the user leaves
  window.addEventListener('beforeunload', function (e) {
    // the absence of a returnValue property on the event will guarantee the browser unload happens
    delete e['returnValue'];
    //console.log('unloading ... ')
    unSetFormSubmitting();
    var formSubmitting = false;
  });

  // closing down here
  console.log("DoIT :: unloading cardsapp.js")
// });