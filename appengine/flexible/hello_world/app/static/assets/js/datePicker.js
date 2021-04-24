const Calendar = document.querySelector('.datepicker')
    M.Datepicker.init(Calendar,{
        format: 'dd mmmm yyyy',
        firstDay: 1,
        minDate: new Date(2021,2,25),
        maxDate: new Date(2021,4,31),
        i18n: {
            cancel: 'Cancelar',
            done: 'Confirmar fecha',
            months: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
                'Mayo',
                'Junio',
                'Julio',
                'Agosto',
                'Septiembre',
                'Octubre',
                'Noviembre',
                'Diciembre',
            ],
            monthsShort: [
                'Ene',
                'Feb',
                'Mar',
                'Abr',
                'May',
                'Jun',
                'Jul',
                'Ago',
                'Sep',
                'Oct',
                'Nov',
                'Dic'
            ],
            weekdaysShort: [
                'Domingo',
                'Lunes',
                'Martes',
                'Miércoles',
                'Jueves',
                'Viernes',
                'Sábado',
            ],
            weekdaysAbbrev:	
            ['D','L','M','M','J','V','S',],
        }
    });