$(function(){
    $('#schedule_val').jqCron({
        enabled_minute: true,
        multiple_dom: true,
        multiple_month: true,
        multiple_mins: false,
        multiple_dow: true,
        multiple_time_hours: false,
        multiple_time_minutes: false,
        default_period: 'week',
        default_value: '0 10-12 * * 1-4,7',
        no_reset_button: false,
        numeric_zero_pad: true,
        lang: 'en',
    });


    var cron =
    $('.cronTime').jqCron({
        enabled_minute: true,
        multiple_dom: true,
        multiple_month: true,
        multiple_mins: false,
        multiple_dow: true,
        multiple_time_hours: false,
        multiple_time_minutes: false,
        default_period: 'week',
        no_reset_button: false,
        numeric_zero_pad: true,
        lang: 'en',
        disabled: true,
    });

});