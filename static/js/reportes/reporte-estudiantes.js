document.addEventListener("DOMContentLoaded", function () {
	const selectAnio = document.getElementById('select_id_year');
	const graficoCanvas = document.getElementById('graficoAlumnosGenero').getContext('2d');
	selectAnio.addEventListener('change', function(){
		const anioSeleccionado = selectAnio.value;
		console.log(anioSeleccionado);
		fetch(`/generar-grafico-barras/${anioSeleccionado}`)
			.then(data => {
				const generos = data.map(item => item.genero);
                const cantidades = data.map(item => item.cantidad);

                new Chart(graficoCanvas, {
                    type: 'bar',
                    data: {
                        labels: generos,
                        datasets: [{
                            label: `Alumnos por Género - ${anioSeleccionado}`,
                            data: cantidades,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.5)',
                                'rgba(54, 162, 235, 0.5)',
                                'rgba(75, 192, 192, 0.5)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(75, 192, 192, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
            });
    });
});

  // Obtener el elemento select
  const select = document.getElementById('select_id_year');

  // Manejar el evento de cambio
  select.addEventListener('change',
	  function () {
		  const selectedOption = select.options[select.selectedIndex];
		  const selectedValue = selectedOption.value;
		  const selectedText = selectedOption.text;

		  // Hacer algo con los valores seleccionados
		  console.log('Valor seleccionado:', selectedValue);
		  console.log('Texto seleccionado:', selectedText);
	  });


document.addEventListener("DOMContentLoaded", () => {
	echarts.init(document.querySelector("#verticalBarChart")).setOption({
		title: {
			subtext: '2022 - 2023',
			left: 'center'
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			}
		},
		legend: {},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
			containLabel: true
		},
		xAxis: {
			type: 'value',
			boundaryGap: [0, 0.01]
		},
		yAxis: {
			type: 'category',
			data: ['Octavo', 'Noveno', 'Décimo', '1ro Bachillerato', '2do Bachillerato', '3ro Bachillerato']
		},
		series: [{
			//name: '2022 - 2023',
			type: 'bar',
			data: [2005, 1990, 1870, 1600, 1500, 1520]
		}
		]
	});
});



