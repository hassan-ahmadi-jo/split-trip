const eventMembersEl = document.getElementById('event-members');
const acceptJoinRequestBtn = document.getElementById('accept-join-request-btn');

const getEnentMemberData = async function(url){
    try {
        const response = await fetch(url, {method: 'GET'});
    if (!response.ok){
        throw new Error('خطا در ثبت اطلاعات')
    };
    
    const result = await response.text();
    
    return result
    } catch (error){
        console.error('Error for geting event members data by ajax', error)
    }
}


const sleep = (seconds) => new Promise(resolve => setTimeout(resolve, seconds));
if (acceptJoinRequestBtn){
    acceptJoinRequestBtn.addEventListener('click', async () => {
        const url = eventMembersEl.dataset.url;
        
        await sleep(100);
        const htmlData = await getEnentMemberData(url);
        
        if (htmlData) {
            eventMembersEl.innerHTML = htmlData;
    }
});
}
