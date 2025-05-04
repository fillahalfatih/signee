/**
 * Dashboard Analytics
 */

'use strict';

(function () {
  let cardColor, headingColor, axisColor, shadeColor, borderColor;

  cardColor = config.colors.cardColor;
  headingColor = config.colors.headingColor;
  axisColor = config.colors.axisColor;
  borderColor = config.colors.borderColor;

  const skorElement = document.getElementById('expensesOfWeek');
  const skorValue = parseFloat(skorElement.getAttribute('value'));

  const elementPg = document.getElementById('kuisPg');
  const skorPg = parseFloat(elementPg.getAttribute('value'));

  const elementInteraktif = document.getElementById('kuisInteraktif');
  const skorInteraktif = parseFloat(elementInteraktif.getAttribute('value'));

  console.log(skorValue + " " + skorPg);
  console.log(skorElement + " " + elementPg);


  // Expenses Mini Chart - Radial Chart
  // --------------------------------------------------------------------
  const weeklyExpensesEl = document.querySelector('#expensesOfWeek'),
    weeklyExpensesConfig = {
      series: [skorValue],
      chart: {
        width: 180, // Perbesar lebar chart
        height: 180, // Perbesar tinggi chart
        type: 'radialBar'
      },
      plotOptions: {
        radialBar: {
          startAngle: 0,
          endAngle: 360,
          strokeWidth: '8',
          hollow: {
            margin: 2,
            size: '60%' // Perbesar ukuran lingkaran dalam
          },
          track: {
            strokeWidth: '200%',
            background: "#a0bbec30"
          },
          dataLabels: {
            show: true,
            name: {
              show: false
            },
            value: {
              formatter: function (val) {
                return parseInt(val); // Tampilkan nilai sebagai persentase
              },
              offsetY: 5,
              color: '#566a7f',
              fontSize: '24px',
              fontFamily: 'Public Sans',
              fontWeight: 600,
              show: true
            }
          }
        }
      },
      fill: {
        type: 'solid',
        colors: "#3368C4"
      },
      stroke: {
        lineCap: 'round'
      },
      grid: {
        padding: {
          top: -10,
          bottom: -15,
          left: -10,
          right: -10
        }
      },
      states: {
        hover: {
          filter: {
            type: 'none'
          }
        },
        active: {
          filter: {
            type: 'none'
          }
        }
      }
    };
  if (typeof weeklyExpensesEl !== undefined && weeklyExpensesEl !== null) {
    const weeklyExpenses = new ApexCharts(weeklyExpensesEl, weeklyExpensesConfig);
    weeklyExpenses.render();
  }

    // Expenses Mini Chart - Radial Chart
  // --------------------------------------------------------------------
  const elementPg1 = document.querySelector('#kuisPg'),
    elementPgConfig = {
      series: [skorPg],
      chart: {
        width: 180, // Perbesar lebar chart
        height: 180, // Perbesar tinggi chart
        type: 'radialBar'
      },
      plotOptions: {
        radialBar: {
          startAngle: 0,
          endAngle: 360,
          strokeWidth: '8',
          hollow: {
            margin: 2,
            size: '60%' // Perbesar ukuran lingkaran dalam
          },
          track: {
            strokeWidth: '200%',
            background: "#a0bbec30"
          },
          dataLabels: {
            show: true,
            name: {
              show: false
            },
            value: {
              formatter: function (val) {
                return parseInt(val); // Tampilkan nilai sebagai persentase
              },
              offsetY: 5,
              color: '#566a7f',
              fontSize: '24px',
              fontFamily: 'Public Sans',
              fontWeight: 600,
              show: true
            }
          }
        }
      },
      fill: {
        type: 'solid',
        colors: "#3368C4"
      },
      stroke: {
        lineCap: 'round'
      },
      grid: {
        padding: {
          top: -10,
          bottom: -15,
          left: -10,
          right: -10
        }
      },
      states: {
        hover: {
          filter: {
            type: 'none'
          }
        },
        active: {
          filter: {
            type: 'none'
          }
        }
      }
    };
  if (typeof elementPg1 !== undefined && elementPg1 !== null) {
    const elementPg = new ApexCharts(elementPg1, elementPgConfig);
    elementPg.render();
  }

    // Expenses Mini Chart - Radial Chart
  // --------------------------------------------------------------------
  const elementInteraktif1 = document.querySelector('#kuisInteraktif'),
    elementInteraktifConfig = {
      series: [skorInteraktif],
      chart: {
        width: 180, // Perbesar lebar chart
        height: 180, // Perbesar tinggi chart
        type: 'radialBar'
      },
      plotOptions: {
        radialBar: {
          startAngle: 0,
          endAngle: 360,
          strokeWidth: '8',
          hollow: {
            margin: 2,
            size: '60%' // Perbesar ukuran lingkaran dalam
          },
          track: {
            strokeWidth: '200%',
            background: "#a0bbec30"
          },
          dataLabels: {
            show: true,
            name: {
              show: false
            },
            value: {
              formatter: function (val) {
                return parseInt(val); // Tampilkan nilai sebagai persentase
              },
              offsetY: 5,
              color: '#566a7f',
              fontSize: '24px',
              fontFamily: 'Public Sans',
              fontWeight: 600,
              show: true
            }
          }
        }
      },
      fill: {
        type: 'solid',
        colors: "#3368C4"
      },
      stroke: {
        lineCap: 'round'
      },
      grid: {
        padding: {
          top: -10,
          bottom: -15,
          left: -10,
          right: -10
        }
      },
      states: {
        hover: {
          filter: {
            type: 'none'
          }
        },
        active: {
          filter: {
            type: 'none'
          }
        }
      }
    };
  if (typeof elementInteraktif1 !== undefined && elementInteraktif1 !== null) {
    const elementInteraktif = new ApexCharts(elementInteraktif1, elementInteraktifConfig);
    elementInteraktif.render();
  }
})();
