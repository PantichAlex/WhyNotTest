var ws=io();
var app=new Vue({
       el: '#app',
        data:function(){
            
            return {
                a:0,
                b:0,
                c:null,
                ws:null
            }
        },
    
        delimiters: ['[[', ']]'],

        created: function(){
            
                ws.on('accept',(data)=>{
                   console.log(data); 
                });
                ws.on('ready',(data)=>{
                    console.log(data);
                    this.c=data.result;
                });
        },

        methods:{
                sum: function(){
            
                     ws.emit('sum', {a:this.a, b:this.b});
                }
        }

        

});
