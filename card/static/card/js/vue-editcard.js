


// reminders
// var reminders = new Vue({
// 	delimiters: ['[[', ']]'],
// 	el: '#vue_reminders',
// 	data: {
// 		open_reminders: ''
// 	},
// 	methods: {
// 		loadData: function () {
// 			$.get('/cards/getreminderscount?card=' + cardid, function (response) {
// 				this.open_reminders = response;
// 			}.bind(this));
// 		}
// 	},
// 	created: function () {
// 		this.loadData();
//
// 		setInterval(function () {
// 			this.loadData();
// 		}.bind(this), 60000);
// 	},
// 	beforeDestroy: function(){
// 		clearInterval(this.interval);
// 	}
// })
