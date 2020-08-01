var ws=io();
var app=new Vue({
       el: '#app',
        data:function(){
            
            return {
                a:0,
                b:0,
                c:null,
                error: null
            }
        },
    
        delimiters: ['[[', ']]'],

        created: function(){
            
                ws.on('accept',(data)=>{
                });
                ws.on('ready',(data)=>{
                    this.c=data.result;
                });

                ws.on('error', (data)=>{
                    this.error=data.message;
                });
        },

        methods:{
                sum: function(){
            
                     this.c=null;
                     this.error=null;
                     ws.emit('sum', {a:this.a, b:this.b});
                }
        }

        

});
