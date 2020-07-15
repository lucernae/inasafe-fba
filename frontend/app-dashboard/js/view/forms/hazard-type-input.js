/**
 * View for handling hazard type input on a form
 */
define([
    'backbone',
    'js/model/depth_class.js',], function (Backbone, HazardClassCollection) {
    return Backbone.View.extend({
        classesByType: {},
        initialize: function ($form) {
            this.classesByType = {}
            this.$input = $form.find('select[name$="hazard_type"]')
            this.$classGuide = $form.find('.hazard-input-guide')
            this.$guideToggler = this.$classGuide.find('.fa')
            this.$classGuideContent = $form.find('.hazard-input-guide-content')

            this.initData()
            this.initEventListener()
        },
        /** Initiate data for hazard selection
         */
        initData: function () {
            // get hazard type list
            const that = this
            hazardTypeCollection.models.forEach(function (model) {
                that.$input.append(`<option data-hazard-type="${model.get('name').toLowerCase()}" value="${model.get('id')}">${model.get('name')}</option>`)
            });

            // get hazard class list
            let classCollection = new HazardClassCollection()
            classCollection.fetch().then(function (data) {
                data.map(x => {
                    if (!x.hazard_type) {
                        x.hazard_type = 1
                    }
                    if (!that.classesByType[x.hazard_type]) {
                        that.classesByType[x.hazard_type] = []
                    }
                    that.classesByType[x.hazard_type].push(x.id)

                    // append the data
                    if (that.$classGuideContent.find(`#hazard-type-${x.hazard_type}`).length === 0) {
                        that.$classGuideContent.append('' +
                            `<table style="width:100%; display: none" id="hazard-type-${x.hazard_type}">` +
                            '   <tr><th>class</th><th>description</th></tr>' +
                            ' </table>')
                    }
                    that.$classGuideContent.find(`#hazard-type-${x.hazard_type}`).append(
                        `<tr><td>${x.id}</td><th>${x.label}</th></tr>`
                    )
                });
                that.$classGuideContent.find(`#hazard-type-${that.$input.val()}`).show()
            }).catch(function (data) {
                console.log('Hazard type request failed');
                console.log(data);
            });
        },
        /**
         * Event placeholder after hazard type are fetched
         */
        onHazardClassFetchDone: function(e){

        },

        /** Initiate event listener
         */
        initEventListener: function () {
            // event listener for guide toggler
            const that = this;
            this.$guideToggler.click(function () {
                that.$classGuideContent.slideToggle()
                if ($(this).hasClass("fa-caret-square-o-down")) {
                    $(this).addClass("fa-caret-square-o-up").removeClass("fa-caret-square-o-down")
                } else {
                    $(this).addClass("fa-caret-square-o-down").removeClass("fa-caret-square-o-up")
                }
            })
            this.$input.change(function () {
                that.$classGuideContent.find('table').hide()
                that.$classGuideContent.find(`#hazard-type-${$(this).val()}`).show()
            })
        },
        /** Get current classes
         */
        returnCurrentClasses: function () {
            return this.classesByType[this.$input.val()]
        },
    });
});
