console.log("main.js 참조");

$(function(){
    // #btn-get-data 인 버튼 찾아서 기능 부여
    $("#btn-get-data").on("click",function(){
        console.log("버튼 클릭");
        
        city_id = document.getElementById('city_id').value;
        local_id = document.getElementById('local_id').value;
        console.log(city_id,local_id);

        if (city_id =="" && local_id ==""){
            alert("시와 구를 다시 확인하세요");
            return;
        }

        // 전달 데이터 생성
        data = {city_id : city_id, local_id : local_id}

        // ajax로 데이터 전달
        $.ajax({
            url: "/getData",
            type: "POST",
            contentType: "application/json", // POST통신
            data: JSON.stringify(data), 
            success: function(response){
                // 성공시 처리
				console.log("응답 결과:", response); // 응답받은 데이터는 json 형태 문자열
				// $('#result').text(response); 

                drawBar(response); 
                // drawBar([5,5,5]); // chart_style.js 에 있는 함수 실행

                

			},
			error: function(error){
				console.log("실패 결과:" , error);
			}
        })

    });
})

// 지역 db 가져오기 -> 도시 datalist 초기화
var location_json;
$.getJSON('static/location.json' , function(json) {
    // 전역 변수에 저장
    location_json = json;

    // 확인
    console.log("지역 json 가져오기" , json); // 전체 데이터 확인
    
    // 현재 html에 임시로 써진 option을 지운다.
    document.getElementById('city').innerHTML = '' 

    // 반복문으로 확인 -> city options 생성
    for(key in location_json){
        console.log(location_json[key])
        $('#city').append("<option value='" + key + "'>"); // 추가
    }
});


$("#city_id").on("change",function(){

    // 구 선택 초기화
    $('#local_id').val('');
    document.getElementById('local').innerHTML = ''


    console.log("선택한 도시 : ",this.value);
    console.log("해당 도시의 구:", location_json[this.value]);
    var locals = location_json[this.value]
    for( index in locals){
        console.log(locals[index]);
        var option_text = $("<option>"+locals[index]+"</option>");
        $('#local').append("<option value='" + locals[index] + "'>"); 
    }
});


// city_id를 재선택할 때 때 초기화하는 이벤트 생성
$("#city_id").focusin(function(){
    $('#city_id').val('');
});

// local_id를 재선택할 때 초기화하는 이벤트 생성
$("#local_id").focusin(function(){
    $('#local_id').val('');
});

