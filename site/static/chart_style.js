

var prev_chart="";

function drawBar(value_data){    
    var canvas = document.getElementById('myChart')
    var ctx = canvas;
    
    // 기존에 그린 것 삭제
    if (prev_chart != ""){
        console.log("기존 삭제")
        prev_chart.destroy()
    }

    // 전달 받은 값들 key 와 value끼리 모으기
    var labels_data = []
    var data_data = []
    var backgroundColor_data = []

    // https://gent.tistory.com/17
    for(key in value_data){
        labels_data.push(key);
        data_data.push(value_data[key]);
        if (value_data[key] < 15){
            backgroundColor_data.push('rgba(0, 255, 0, 1)'); // 안전 수치일 때 - 녹색
        }
        else if(value_data[key] < 30){
            backgroundColor_data.push('rgba(255, 127, 0, 1)') // 주의 수치일 때 주황
        }
        else{
            backgroundColor_data.push('rgba(255, 0, 0, 1)') // 위험 수치일 때 빨강
        }
    }

    console.log("분리된 데이터 : " , labels_data, data_data)

    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
            labels: labels_data, // ['첫번째 수', '두번째 수', '세번째 수'],
            datasets: [{
                label: '예측된 오늘의 범죄율',
                backgroundColor: backgroundColor_data, //'rgb(255, 99, 132)',
                borderColor: 'rgb(0, 0, 0)',
                data: data_data // [0, 10, 5]
            }]
        },
        // Configuration options go here
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }]
            }
        }
    });

    // 현재 차트를 이전 차트로 저장
    prev_chart = chart;

    canvas.style.backgroundColor = "rgba(255,255,255, 1)";
    canvas.style.boxShadow = "5px 5px 10px -2px rgba(0, 0, 0, 1)";
    canvas.style.marginBottom = "50px";
    
}

