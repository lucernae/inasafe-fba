define([
    'backbone',
    'moment'
], function (Backbone) {

    const AdministrativeCountryMapping = Backbone.Model.extend({
        initialize: function (region_level){
            this.region_level = region_level;
        },
        url: function () {
            return `${postgresUrl}vw_administrative_country_mapping_${this.region_level}_filter?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: AdministrativeCountryMapping,
        initialize: function (region_level){
            this.region_level = region_level;
        },
        url: function () {
            return `${postgresUrl}vw_administrative_country_mapping_${this.region_level}_filter`;
        },
        findByIds: function (ids){
            let url = this.url();
            let filter = `?${this.region_level}_id=in.(${ids.join()})`;
            return this.fetch({
                url: `${url}${filter}`
            });
        }
    });
});
