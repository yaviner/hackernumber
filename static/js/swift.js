$(document).ready(function(){
	$('#trigger-button').click(function(){
		$('#top-area').animate({marginTop: '-300px'}, 1000).promise(showLoading());
		var username = $('#main-input').val();
		if(username == 'theycallmeswift'){
			var swiftAnswer = "<div id='answer-number'>0</div>";
			swiftAnswer += "<div id='answer-text'>At your service, Mr. Gosling.</div>";
			$('#answer').append(swiftAnswer);
		}else{
			var loc = "/compare"+username;
			doAjax(username);
		}
	});
});

function doAjax(username){
	var blah = $.ajax({
				dataType: "json",
				url: "/test",
				type: "GET",
				async: false
			}).responseText;
	var str = "var x = " + blah;
	var blah2 = [
			{
				user: "yaviner",
				repo: "pokerama"
			},
			{
				user: "jromer94",
				repo: "hackernumber"
			}
		]
	eval(str);
	parse(x);

}
function showLoading(){
	$('#loading-gif').show(1500);
}

function parse(mock){
	console.log("hey");
	$.each(mock, function(index, value){
		if(index == mock.length-1){
			var appended = "<div class='result-name result isSwift'>"+this.user+"</div>";
		}else{
			var appended = "<div class='result-name result'>"+this.user+"</div>";
			appended += "<div class='result-repo result'>"+this.repo+"</div>";
		}
		$('#returnResults').append(appended);
	});
	determineSwiftNumber(mock);
	$('#loading-gif').hide(1500);
}

function determineSwiftNumber(mock){
		var swiftNumber = mock.length;
		console.log(mock);
		console.log(swiftNumber);
			switch(swiftNumber){
				case 5:
					var swiftAnswer = "<div id='answer-number'>5</div>";
					swiftAnswer += "<div id='answer-text'>You are straddling the line of non-existence.</div>";
					$('#answer').append(swiftAnswer);
					break;
				case 4:
					var swiftAnswer = "<div id='answer-number'>4</div>";
					swiftAnswer += "<div id='answer-text'>Good luck getting a job, poser.</div>";
					$('#answer').append(swiftAnswer);
					break;
				case 3:
					var swiftAnswer = "<div id='answer-number'>3</div>";
					swiftAnswer += "<div id='answer-text'>Three repos away? Have you even ever been to a hackathon?</div>";
					$('#answer').append(swiftAnswer);
					break;
				case 2:
					var swiftAnswer = "<div id='answer-number'>2</div>";
					swiftAnswer += "<div id='answer-text'>Two repos away? Not bad. For a rookie.</div>";
					$('#answer').append(swiftAnswer);
					break;
				case 1:
					var swiftAnswer = "<div id='answer-number'>1</div>";
					swiftAnswer += "<div id='answer-text'>You are a true fanboy.</div>";
					$('#answer').append(swiftAnswer);
					break;
				default:
					var swiftAnswer = "<div id='answer-number'>5+</div>";
					swiftAnswer += "<div id='answer-text'>Do you even write code, bro?</div>";
					$('#answer').append(swiftAnswer);
					break;
			}
		};