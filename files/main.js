function func(n,S){
    n = S.length;
    let num = []
    for(let i=0; i<n; i++){
        let count = 0;
        while (S[i] == 'a') {
            count = 1;
            if(S[i] == S[i+1]){
                count++;
            }
        }
        if(count != 0){
            num.push(count);
        }
    }
num.sort(function(a,b){
    if(a>b){
        return a
    }
})

console.log(num)

}

console.log(func(10,'sasaaadsaa'))
