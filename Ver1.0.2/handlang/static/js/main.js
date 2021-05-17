$(document).ready(function()  {
	// 라벨 측정 시작
	$(document).keypress(function(event){  // keyup 이벤트 처리 enter, backspace
		var correct = 0;
		var total_correct = 0;
		var timer;
		function check_correct(lang_code)	{
			total_correct++;
			
			if (total_correct>= 8)	{
				$("#check_table_"+total_correct).attr("src", "../static/img/smile.png");
				clearInterval(timer);
				if(lang_code=="en"){
					$("#predict_status").text("✅ done ✅");    //js도 언어 바꾸기 1. jinja 내부에 넣기 or 2. session에서 가져와서 하는 방법
		
				}
				else if(lang_code=="ko"){
					$("#predict_status").text("✅ 연습완료! 예측을 중지합니다. ✅");    //js도 언어 바꾸기 1. jinja 내부에 넣기 or 2. session에서 가져와서 하는 방법
				}
			}
			else $("#check_table_"+total_correct).attr("src", "../static/img/smile.png");
		}





		function ajax_prediction(save_langcode){
			var alphabet = $("#topic").text();
		
			console.log('ajax!');
			$.ajax({
			  url: '/return_label',
			  type: 'POST', 
			  data: {
				  target: alphabet
			  },
			  dataType: 'JSON',
			  success: function(result){
				save_langcode(result.lang_code);
				  console.log(result);
				  $("#predict-in").text(result.info + result.label);
				  if(result.status === 0) {
					  correct = 0;
				  }
				  else	{
					  correct++;
					  console.log("플러스");
					  if(correct === 3)	{
						  check_correct(result.lang_code);
						  correct = 0;
					  }
				}
		 
			  
			},
			  error: function(xtr, status, error){
				  console.log(xtr+":"+status+":"+error);
			  }
			});
		
		}


		
		var keycode = (event.keyCode ? event.keyCode : event.which);

		if(keycode === 13) {
			console.log('엔터!');

			timer=setInterval(function(){
				ajax_prediction(function (lang_code) {
					if (lang_code == "en") {
						$("#predict_status").text("🔆 Predicting... 🔆");

					} else if (lang_code == "ko") {
						$("#predict_status").text("🔆 예측중... 🔆");

					}

				});	

			}, 1000);

		}

	});


});



