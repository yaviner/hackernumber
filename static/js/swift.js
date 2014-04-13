$(document).ready(function(){
	$('#trigger-button').click(function(){
		$('#top-area').animate({marginTop: '-300px'}, 1000).promise(showLoading());
	});
});

function showLoading(){
	$('#loading-gif').show(1500);
}