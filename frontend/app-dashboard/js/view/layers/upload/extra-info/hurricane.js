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
                return {
                }
            },
            get_hazard_type: function () {
                return 'hurricane';
            }
        })
    })
