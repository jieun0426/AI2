package com.example.AI2.dto;

import com.example.AI2.entity.JudgEntity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class JudgDTO {
    String doc_class;
    String doc_id;
    String casenames;
    String normalized_court;
    String casetype;
    String sentences;
    String announce_date;

    public JudgEntity entity(){
        return new JudgEntity(doc_id,doc_class,casenames,normalized_court,casetype,
                sentences, announce_date);
    }
}
