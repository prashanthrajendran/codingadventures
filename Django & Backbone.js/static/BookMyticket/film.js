
	var MovieView = Backbone.View.extend({
		el : '#mdiv',
		template: _.template($('#movie-template').html()),
		initialize: function(){
			this.collection = new Movies();
			this.collection.bind("reset", this.render, this);
			this.collection.fetch();
		},
		render:function(){
			this.$el.html( this.template( {movielist:this.collection.toJSON()} ) );
			$(".chzn-select12").chosen();
		}		
	});
	
	var Movie = Backbone.Model.extend({
		defaults:{
			language : '',
			movies : []
		}
	});
	
	var Movies = Backbone.Collection.extend({
		model : Movie,
		url : "http://localhost:8000/service/",
	});

	var view = new MovieView();