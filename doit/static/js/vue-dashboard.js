
// my_cards
var my_open = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my_vue_cards',
	data: {
		my_open_cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/my_vue_cards', function (response) {
				this.my_open_cards = response.open_cards;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 20000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})

// my_overdue_cards
var my_overdue = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my_vue_overdue',
	data: {
		my_overdue_cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/my_vue_overdue', function (response) {
				this.my_overdue_cards = response.overdue_cards;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 20000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})
