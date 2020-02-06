$( document ).ready(function() {

	$('input').on('blur',function(){
		var data= [];
		$.each( $('input'), function( index, tag ){
		   	data.push(tag.value);
		});
		
		console.log(data);
		$.post("/check", JSON.stringify(data), function(data, status){
			var obj = JSON.parse(data);
			console.log(obj.message)
			if(obj.message==undefined){
				document.getElementById("lilfooty").textContent = "Connection Error";
			}
			if(obj.message=="None"){
				document.getElementById("lilfooty").textContent = "SNMP Timeout/Configuration Error";
			}
			else{
				document.getElementById("lilfooty").innerHTML = obj.message;
			}
		});
	});
});
