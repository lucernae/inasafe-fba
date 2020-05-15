define([
    'backbone',
    'underscore',
    'jquery',
    'moment',
    'js/model/flood.js',
    'js/model/forecast_event.js',
    'js/view/forms/hazard-type-input.js'
], function (Backbone, _, $, moment, FloodModel, ForecastEvent, HazardTypeInput) {
    return Backbone.View.extend({
        el: "#upload-flood-form",
        events: {
            'submit': 'submitForm'
        },

        initialize: function(){
            this.progressbar = this.$el.find("#upload-progress-bar");
            this.progressbar.hide();
            const $form = this.$el;
            this.$place_name = $form.find("input[name='place_name']");
            this.$source = $form.find("input[name='source']");
            this.$event_notes = $form.find("input[name='event_notes']");
            this.$flood_model_notes = $form.find("input[name='flood_model_notes']");
            this.$source_url = $form.find("input[name='source_url']");
            this.$geojson = $form.find("input[name='geojson']");
            this.$return_period = $form.find("select[name='return_period']");
            this.$acquisition_date = $form.find("input[name='acquisition_date']");
            this.$forecast_date = $form.find("input[name='forecast_date']");
            this.$hazard_type = $form.find("select[name='hazard_type']");
            this.hazardInput = new HazardTypeInput($('#upload-flood-form'));
        },

        submitForm: function(e){
            e.preventDefault();
            this.$el.find('[type=submit]').hide();
            this.progressbar.show();
            const that = this;

            // make flood model map
            const place_name = this.$place_name.val();
            const source = this.$source.val();
            const event_notes = this.$event_notes.val();
            const flood_model_notes = this.$flood_model_notes.val();
            const source_url = this.$source_url.val();
            const geojson = this.$geojson[0].files;
            const return_period = this.$return_period.val();
            const acquisition_date = moment.fromAirDateTimePicker(this.$acquisition_date.val()).format();
            const forecast_date = moment.fromAirDateTimePicker(this.$forecast_date.val()).format();
            const hazard_type = this.$hazard_type.val();

            const forecast_event_attr = {
                source: source,
                link: source_url,
                notes: event_notes,
                acquisition_date: acquisition_date,
                forecast_date: forecast_date,
                hazard_type_id: hazard_type
            };

            const forecast_event = new ForecastEvent(forecast_event_attr);
            this.forecast_event = forecast_event;
            
            FloodModel.uploadFloodMap({
                files: geojson,
                place_name: place_name,
                return_period: return_period,
                flood_model_notes: flood_model_notes,
                hazard_classes: that.hazardInput.returnCurrentClasses()
            })
                .then(function(flood){
                    that.flood = flood;

                    // attach handler
                    that.flood.on('upload-finished', that.uploadFloodFinished, that);
                    that.flood.on('feature-uploaded', that.updateProgress, that);
                    that.setProgressBar(0);

                }).catch(function (error) {
                    console.log(error);
                    if("message" in error){
                        let message = error.message;
                        alert("Upload Failed. " + message);
                    }
                    else {
                        alert("Upload Failed. GeoJSON file parsing failed");
                    }
                    that.$el.find('[type=submit]').show();
                    that.progressbar.hide();
            });
            return false;
        },

        uploadFloodFinished: function (layer) {
            // upload forecast event
            const that = this;
            let options = {
                'headers': {
                    'prefer': 'return=representation'
                }
            };
            this.forecast_event.save(
                {
                    flood_map_id: layer.get('id'),
                    queue_status: 0
                }, options)
                .then(function (response, textStatus) {
                    if(response){
                        console.log(response)
                        // parser error but successfully sent to server
                        alert('Flood map successfully uploaded! It might take a while until the process finished.');
                        that.$el.find('[type=submit]').show();
                        $('form').trigger('reset');
                        that.progressbar.hide();
                    }
                    else if(textStatus !== 'success') {
                        alert('Upload Failed. Forecast information failed to save');
                        that.$el.find('[type=submit]').show();
                        that.progressbar.hide();
                    }
                })
                .fail(function(response, textStatus)
                {
                    console.log(response)
                });

        },
        triggerCalculation: function (id) {
            AppRequest.post(postgresBaseUrl + '/rpc/kartoza_fba_forecast_glofas_update_trigger_status',
                {
                    'hazard_event_id': id
                }
            ).then(function (value) {
                console.log(value)
            })
        },
        setProgressBar: function(value){
            this.progressbar.find(".progress-bar")
                .css("width", value+"%")
                .attr("aria-valuenow", value)
                .attr("aria-valuemin", 0)
                .attr("aria-valuemax", 100);
        },

        updateProgress: function (feature) {
            if(this.flood.featureCount() > 0){
                let progress = this.flood.uploadedFeatures() * 100 / this.flood.featureCount();
                this.setProgressBar(progress);
            }
        }
    })
})
