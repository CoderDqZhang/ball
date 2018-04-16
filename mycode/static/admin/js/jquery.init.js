<<<<<<< HEAD
/*global django:true, jQuery:false*/
=======
>>>>>>> 7c72ceb493cd818bbe206050de3c2bb4cffa99d6
/* Puts the included jQuery into our own namespace using noConflict and passing
 * it 'true'. This ensures that the included jQuery doesn't pollute the global
 * namespace (i.e. this preserves pre-existing values for both window.$ and
 * window.jQuery).
 */
var django = django || {};
django.jQuery = jQuery.noConflict(true);
