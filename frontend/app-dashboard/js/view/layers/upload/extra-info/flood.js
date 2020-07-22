define([
    'backbone',
    'leaflet',
    'jquery',
    'wellknown'],
    function (Backbone, L, $, Wellknown) {
        return Backbone.View.extend({
            initialize: function($form){
                this.$el = $form;
            },
            get_extra_info: function () {
                this.$return_period = this.$el.find("[name='return_period']");
                return {
                    return_period: this.$return_period.val()
                }
            },
            get_hazard_type: function () {
                return 'flood';
            }
        })
    })
