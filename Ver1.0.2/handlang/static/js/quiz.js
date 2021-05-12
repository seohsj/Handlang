
$(document).ready(function(){
	var q_num=0;
	var total_q=5;
	//$("#"+q_num).show();

	$("#next").click(function(){
	  $("#before").show();

	  $("#"+q_num).hide();
	  
	  q_num+=1;
	  console.log(q_num);
	//   location.href = "#"+q_num;
	  

	  if(q_num==total_q-1){
		$('#next').hide();
		$('#submit').show();
	  }
	   $("#"+q_num).toggle();
	

	});


	$("#before").click(function(){

	  $("#submit").hide();
	  $("#next").show();
	 $("#"+q_num).hide();
	  q_num=q_num-1;
	  console.log(q_num);

	  if(q_num==0){
		$('#before').hide();
	  }
	  $("#"+q_num).toggle()
	
	});

});