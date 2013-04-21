/**
 *  Module
 *
 * Description
 */
angular.module('components', [])
.directive('loading', function() {
	return {
		restrict: 'E',
		scope: {
			label: "=",
			interval: "="
		},
		link: function(scope, element) {
			var states = [".", "..", "..."];
			var currentState = 0;
			var counter = 0;

			var update = function(state) {
				var text = scope.label + " " + states[currentState];
				angular.element(element).text(text);
			};

			setInterval(function () {
				currentState = counter%states.length;
				counter += 1;
				update(currentState);
			}, scope.interval);
		}
	};
})
.directive('copyright', function(){
  return {
    restrict: 'E',
    scope: {
      label: "=",
      start: "="
    },
    link: function(scope, element){
      var currentDate = new Date();
      var currentYear = currentDate.getFullYear();
      
      var text = "© " + scope.start + " — " + currentYear + " " +  scope.label; 
      if (scope.start == currentYear) {
        text = "© " + scope.start + " " + scope.label;
      }
      
      angular.element(element).text(text);
    }
  };
});