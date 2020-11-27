$(document).ready(function() { 
		$('#hi1').on('submit',function(event) { 
			$.ajax({
			data : {
				userid : $('#id11').val(),
				count1 : $('#count11').val(),
				postid : $('#post11').val()
			},
			type : 'POST',
			url : '/vote'
		})
		.done(function(data) {

			if (data.error) {
				alert("You have alreday voted.")
			}
			else {
				$("#vote00").text(data.count);
			}
		});

		event.preventDefault();
	}); 
}); 