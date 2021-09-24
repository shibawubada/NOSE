from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        #return current process
        return self.processes[cur_event.process_id]
                          
    def dispatcher_func(self, cur_process):
        #change state and run in order of arrival from scheduler
        cur_process.process_state = ProcessStates.RUNNING            
        cur_process.run_for(cur_process.service_time,self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        #return new event       
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, 
                     event_time=cur_process.departure_time)
    
class SJF(SchedulerDES):
    def scheduler_func(self, cur_event): 
        #ready process list
        processQ = []
        for process in self.processes:
            if process.process_state == ProcessStates.READY:
                processQ.append(process)
        #sort and return    
        return min([x for x in processQ], key=lambda x: x.remaining_time)
        
    def dispatcher_func(self, cur_process):
        #change state and run in order of arrival from scheduler                        
        cur_process.process_state = ProcessStates.RUNNING            
        cur_process.run_for(cur_process.service_time,self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        #return new event       
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, 
                     event_time=cur_process.departure_time)

class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        #return current process
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
       
        cur_process.process_state = ProcessStates.RUNNING       
        run_time = cur_process.run_for(self.quantum,self.time)
        time = run_time+self.time
        #change finished procceses to terminated, proceses still to be completed are set to ready
        if cur_process.remaining_time<=0:
                      
            cur_process.process_state = ProcessStates.TERMINATED
            #return new event
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, 
                         event_time=cur_process.departure_time)
        else:
            cur_process.process_state = ProcessStates.READY
            #return new event            
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, 
                         event_time=time)

class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        #ready process list
        processQ = []
        for process in self.processes:
            if process.process_state == ProcessStates.READY:
                processQ.append(process)
        #sort and return      
        return min([x for x in processQ], key=lambda x: x.remaining_time)


    def dispatcher_func(self, cur_process):

        cur_process.process_state = ProcessStates.RUNNING       
        run_time = cur_process.run_for(min(cur_process.remaining_time, self.next_event_time() - self.time), self.time)
        time = run_time+self.time
        #change finished procceses to terminated, proceses still to be completed are set to ready
        if cur_process.remaining_time<=0:
                       
            cur_process.process_state = ProcessStates.TERMINATED
            #return new event
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, 
                         event_time=cur_process.departure_time+self.context_switch_time)
        
        elif self.next_event_time()<=time:
            cur_process.process_state = ProcessStates.READY
            #return new event         
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, 
                         event_time=time+self.context_switch_time)    