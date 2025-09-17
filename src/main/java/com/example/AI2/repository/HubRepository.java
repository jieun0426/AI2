package com.example.AI2.repository;

import com.example.AI2.entity.HubEntity;
import com.example.AI2.entity.JudgEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HubRepository extends JpaRepository<HubEntity, String> {
    @Query(value="select count(*) as 환자수 from hubdata where content like %:keyword%", nativeQuery = true)
    int countByKeyword(String keyword);

    @Query(value="select * from hubdata where content like %:keyword%", nativeQuery = true)
    List<HubEntity> findAllByKeyword(String keyword);

    @Query(value = "SELECT * FROM (SELECT t.*, ROWNUM rnum FROM (SELECT * FROM hubdata ORDER BY num DESC) t WHERE ROWNUM <= :end) " +
            "WHERE rnum > :start ORDER BY num DESC", nativeQuery = true)
    List<HubEntity> findByPage(@Param("start") int start, @Param("end") int end);

    @Query(value = "SELECT * FROM (SELECT t.*, ROWNUM rnum FROM (SELECT * FROM hubdata where content like %:keyword% ORDER BY num DESC) t " +
            "WHERE ROWNUM <= :end) WHERE rnum > :start ORDER BY num DESC", nativeQuery = true)
    List<HubEntity> findKeywordByPage(@Param("start") int start, @Param("end") int end, String keyword);

    @Query(value = "SELECT COUNT(*) FROM hubdata", nativeQuery = true)
    int countAll();
}
